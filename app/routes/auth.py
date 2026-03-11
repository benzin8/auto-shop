from flask import Blueprint, render_template, request, redirect, url_for
from app.services.registration import register_user as reg, login_user_service as log, logout_user_service as logout

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET'])
def registration():
    return render_template('auth/register.html')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    result = reg(username, email, password)

    if result is True:
        return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html', error=result)

@auth_bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html')

@auth_bp.route('/login', methods=['POST'])
def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    user = log(username, password)
    if user:
        return redirect(url_for('shop.index'))
    else:
        return render_template('auth/login.html', error="Неверное имя пользователя или пароль")
    
@auth_bp.route('/logout', methods=['GET'])
def logout_user():
    logout()
    return redirect(url_for('auth.login'))

