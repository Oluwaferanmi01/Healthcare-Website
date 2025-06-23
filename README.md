# Healthcare-Website
A website to collect user details
# 🩺 VMedix – Income & Spending Survey App

VMedix is a Flask-based web application designed to collect user demographic data and income/expense information. Users can sign up, log in, fill out a detailed financial survey, and export the data to CSV. The app also supports data visualization using `matplotlib` and `pandas`.

---

## 📦 Features

- ✅ User authentication (Sign up / Login / Logout)
- ✅ Secure password hashing with `bcrypt`
- ✅ MongoDB for user and survey data
- ✅ Bootstrap-powered responsive UI
- ✅ Dark Mode toggle
- ✅ Income and optional expenses survey form
- ✅ CSV export functionality
- ✅ Visualizations (PNG charts saved via `matplotlib`)
- ✅ Flash messages and session-based access

---

## 🚀 Tech Stack

| Component     | Technology         |
| ------------- | ------------------ |
| Backend       | Python + Flask     |
| Database      | MongoDB            |
| Frontend      | HTML, CSS, Bootstrap 5 |
| Visualization | Matplotlib, Pandas |
| Auth          | Flask sessions + Bcrypt |

---

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/vmedix.git
cd vmedix

### 2. Setup a Virtual Environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Start MongoDB

### 5. Run the application
python app.py

### 6. Generate Visualizations
python visualize.py

