from flask import Blueprint, render_template, flash, request, abort, redirect, url_for, current_app
from app.core.database import db
from app.models.products import Product
from app.models.brands import Brand
from app.models.categories import Category
from app.models.orders import Order
from app.models.users import User
from flask_login import current_user, login_required

from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint('dashboard', __name__)

@admin_bp.route('/')
def dashboard():
    return render_template('main_page.html')

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if current_user.role != 'admin':
        abort(403)

    if request.method == 'POST':
        sku = request.form.get('sku')
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        brand_id = request.form.get('brand_id')
        category_id = request.form.get('category_id')
        image = request.files.get('image')

        image_path = 'static/product_images/default.jpg'
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'product_images')
            os.makedirs(upload_folder, exist_ok=True)
            image.save(os.path.join(upload_folder, filename))
            image_path = f'static/product_images/{filename}'

        new_prod = Product(
            sku=sku,
            name=name,
            description=description,
            price=price,
            brand_id=brand_id,
            category_id=category_id,
            image_path=image_path
        )
        db.session.add(new_prod)
        db.session.commit()
        return redirect(url_for('shop.index'))

    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('dashboard/add_products.html', brands=brands, categories=categories)

@admin_bp.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'admin':
        abort(403)
        
    product = db.session.get(Product, product_id)
    if not product:
        abort(404)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.sku = request.form.get('sku')
        product.description = request.form.get('description')
        product.price = request.form.get('price')
        product.brand_id = request.form.get('brand_id')
        product.category_id = request.form.get('category_id')
        
        image = request.files.get('image')
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'product_images')
            image.save(os.path.join(upload_folder, filename))
            product.image_path = f'static/product_images/{filename}'

        db.session.commit()
        return redirect(url_for('shop.index'))

    brands = Brand.query.all()
    categories = Category.query.all()
    return render_template('dashboard/edit_product.html', product=product, brands=brands, categories=categories)

@admin_bp.route('/users')
@login_required
def list_users():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('dashboard/list_users.html', users=users)

# Роут для смены роли пользователя
@admin_bp.route('/change_role/<int:user_id>', methods=['POST'])
@login_required
def change_role(user_id):
    if current_user.role != 'admin':
        abort(403)
    
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    
    if new_role in ['user', 'manager', 'admin']:
        user.role = new_role
        db.session.commit()
        flash(f'Роль пользователя {user.username} изменена на {new_role}', 'success')
    
    return redirect(url_for('dashboard.list_users'))

# Роут для менеджера заказов (Менеджер и Админ)
@admin_bp.route('/orders')
@login_required
def manager_orders():
    if current_user.role not in ['manager', 'admin']:
        abort(403)
    # Загружаем заказы вместе с данными пользователей, чтобы не делать лишних запросов
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('dashboard/manager_orders.html', orders=orders)

@admin_bp.route('/update_order_status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    # Проверяем права: только менеджер или админ
    if current_user.role not in ['manager', 'admin']:
        abort(403)
    
    # Ищем заказ в базе
    order = Order.query.get_or_404(order_id)
    
    # Получаем новый статус из формы
    new_status = request.form.get('status')
    
    # Список допустимых статусов (для безопасности)
    valid_statuses = ['pending', 'processing', 'completed', 'canceled']
    
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f'Статус заказа #{order_id} успешно обновлен на "{new_status}"', 'success')
    else:
        flash('Попытка установить недопустимый статус!', 'danger')
        
    # Возвращаемся обратно на страницу заказов менеджера
    return redirect(url_for('dashboard.manager_orders'))