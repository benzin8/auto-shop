from flask import Flask
from flask_admin import Admin
from app.core.admin_access import AdminModelView, MyAdminIndexView

from flask_login import LoginManager

from pathlib import Path
from app.core.config import load_settings
from app.core.database import db

from app.models.categories import Category
from app.models.brands import Brand
from app.models.products import Product
from app.models.users import User
from app.models.orders import Order, OrderComposition
from app.models.cars import Car
from app.models.compatibitily import Compatibility


from app.routes.shop import shop_bp
from app.routes.admin import admin_bp
from app.routes.auth import auth_bp
from app.routes.user import user_bp

login_manager = LoginManager()

def create_app():
    template_dir = Path(__file__).parent.parent / 'templates'
    app = Flask(__name__, template_folder=str(template_dir))
    settings = load_settings()
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['FLASK_ADMIN_TEMPLATE_MODE'] = 'bootstrap4'
    app.config['SECRET_KEY'] = settings.secret_key

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.registration'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    admin_panel = Admin(app, 
        name="Администратор",
        index_view=MyAdminIndexView(),
        )

    admin_panel.add_view(AdminModelView(Product, db.session, "Товары"))
    admin_panel.add_view(AdminModelView(Brand, db.session, "Бренды"))
    admin_panel.add_view(AdminModelView(Category, db.session, "Категории товаров"))
    admin_panel.add_view(AdminModelView(User, db.session, "Пользователи"))
    admin_panel.add_view(AdminModelView(Order, db.session, "Заказы"))
    admin_panel.add_view(AdminModelView(OrderComposition, db.session, "Состав заказов"))
    admin_panel.add_view(AdminModelView(Car, db.session, "Автомобили"))
    admin_panel.add_view(AdminModelView(Compatibility, db.session, "Совместимость"))

    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp, url_prefix='/dashboard')
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')

    with app.app_context():
        db.create_all()
    
    return app