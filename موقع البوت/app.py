from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('main.html')

# صفحة اللوغين
@app.route('/login')
def login():
    return render_template('login.html')

# صفحة داشبورد
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# صفحة الإعدادات
@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == "__main__":
    app.secret_key = 'YOUR_SECRET_KEY'  # تأكد من إضافة مفتاح سري
    app.run(debug=True)
