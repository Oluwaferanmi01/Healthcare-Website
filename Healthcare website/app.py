from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import csv
from datetime import datetime
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))  # Secure session key

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Check connection
    db = client['income_spending_db']
    users_collection = db['users']
    survey_collection = db['survey_data']
except ConnectionFailure:
    print("Error: MongoDB is not available.")
    exit(1)

# User data class
class User:
    def __init__(self, age, gender, total_income, expenses, username):
        self.age = age
        self.gender = gender
        self.total_income = total_income
        self.expenses = expenses
        self.username = username

    def to_dict(self):
        return {
            'username': self.username,
            'age': self.age,
            'gender': self.gender,
            'total_income': self.total_income,
            'expenses': self.expenses,
            'timestamp': datetime.now()
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        flash('Please log in to access the survey.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            gender = request.form['gender']
            total_income = float(request.form['income'])

            expenses = {
                'utilities': float(request.form.get('utilities', 0)),
                'entertainment': float(request.form.get('entertainment', 0)),
                'school_fees': float(request.form.get('school_fees', 0)),
                'shopping': float(request.form.get('shopping', 0)),
                'healthcare': float(request.form.get('healthcare', 0))
            }

            user = User(age, gender, total_income, expenses, session['username'])
            survey_collection.insert_one(user.to_dict())

            # Save to CSV
            with open('user_data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if csvfile.tell() == 0:
                    writer.writerow(['username', 'age', 'gender', 'total_income', 'utilities',
                                     'entertainment', 'school_fees', 'shopping', 'healthcare'])
                writer.writerow([session['username'], age, gender, total_income,
                                 expenses['utilities'], expenses['entertainment'],
                                 expenses['school_fees'], expenses['shopping'], expenses['healthcare']])

            flash('Survey submitted successfully!', 'success')
            return redirect(url_for('thank_you'))

        except ValueError:
            flash('Invalid input. Please fill all fields correctly.', 'danger')

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        user = users_collection.find_one({'username': username})
        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        confirm_password = request.form['confirm_password'].encode('utf-8')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
        elif users_collection.find_one({'username': username}):
            flash('Username already exists.', 'danger')
        elif users_collection.find_one({'email': email}):
            flash('Email already in use.', 'danger')
        else:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            users_collection.insert_one({
                'username': username,
                'email': email,
                'password': hashed_password
            })
            flash('Signup successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/thank-you')
def thank_you():
    if 'username' not in session:
        flash('Please log in to view this page.', 'warning')
        return redirect(url_for('login'))
    return render_template('thank_you.html')

@app.route('/export')
def export_csv():
    if 'username' not in session:
        flash('Please log in to export data.', 'warning')
        return redirect(url_for('login'))

    export_dir = 'data'
    os.makedirs(export_dir, exist_ok=True)
    file_path = os.path.join(export_dir, 'exported_data.csv')

    try:
        users = survey_collection.find()
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'age', 'gender', 'total_income',
                             'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare'])

            for user in users:
                expenses = user.get('expenses', {})
                writer.writerow([
                    user.get('username', ''),
                    user.get('age', ''),
                    user.get('gender', ''),
                    user.get('total_income', ''),
                    expenses.get('utilities', ''),
                    expenses.get('entertainment', ''),
                    expenses.get('school_fees', ''),
                    expenses.get('shopping', ''),
                    expenses.get('healthcare', '')
                ])
        flash("Data exported successfully!", "success")
    except Exception as e:
        flash(f"Export failed: {str(e)}", "danger")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


