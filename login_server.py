from flask import Flask, redirect, url_for, session, request
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # 🔒 استبدله بكلمة سر عشوائية قوية

# إعداد OAuth
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # <-- مهم
    client_kwargs={'scope': 'openid email profile'},
)

# صفحة تسجيل الدخول
@app.route('/login')
def login():
    return '''
        <h3>Login</h3>
        <a href="/login/google">Login with Google</a>
    '''

# بدء تسجيل الدخول عبر Google
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

# المعالجة بعد تسجيل الدخول
@app.route('/login/google/callback')
def authorize_google():
    token = oauth.google.authorize_access_token()
    userinfo = oauth.google.get('userinfo').json()  # ✅ استبدال parse_id_token
    session['user'] = userinfo
    return f'✅ Logged in as: {userinfo["email"]}'

# تشغيل السيرفر
if __name__ == '__main__':
    app.run(debug=True)
