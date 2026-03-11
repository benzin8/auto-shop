from app.models.users import User
from app.core.database import db
from flask_login import login_user, logout_user

def register_user(username, email, password):
    if db.session.execute(db.select(User).filter_by(username=username)).scalar():
        return "Имя пользователя уже занято"
    if db.session.execute(db.select(User).filter_by(email=email)).scalar():
        return "Email уже зарегистрирован"
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return True

def login_user_service(username, password):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
    if user and user.check_password(password):
        login_user(user, remember=True)
        return user
    return False

def logout_user_service():
    logout_user()
    return True

