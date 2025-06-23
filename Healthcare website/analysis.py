from pymongo import MongoClient
import csv

class User:
    def _init_(self, age, gender, total_income, expenses):
        self.age = age
        self.gender = gender
        self.total_income = total_income
        self.expenses = expenses

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['vmedix_db']
collection = db['users']

# Export data to CSV
with open('user_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['age', 'gender', 'total_income', 'utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare'])
    for user in collection.find():
        writer.writerow([
            user['age'], user['gender'], user['total_income'],
            user['expenses']['utilities'], user['expenses']['entertainment'],
            user['expenses']['school_fees'], user['expenses']['shopping'], user['expenses']['healthcare']
        ])
print("Data exported to user_data.csv")