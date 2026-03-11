from collections import Counter
from flask import Blueprint, render_template
from app.core.database import db
from app.models.products import Product
from flask_login import current_user
from app.models.orders import Order, OrderComposition

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/products')
def index():
    products = db.session.execute(db.select(Product)).scalars().all()
    if current_user.is_authenticated and current_user.role == "admin":
        return render_template('shop/index.html', products=products)
    return render_template('shop/index.html', products=products)

@shop_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return render_template('shop/product_not_found.html'), 404
    return render_template('shop/product_detail.html', product=product)

from flask import session, redirect, url_for, request, render_template, flash
from flask_login import current_user, login_required

# 1. Добавление в корзину
@shop_bp.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    # Просто добавляем ID товара в список в сессии
    cart = session['cart']
    cart.append(product_id)
    session['cart'] = cart
    
    flash("Товар добавлен в корзину!")
    return redirect(url_for('shop.index'))

# 2. Просмотр корзины
@shop_bp.route('/cart')
def view_cart():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return render_template('shop/cart.html', products=[], total=0)
    
    counts = Counter(cart_ids)
    
    # Получаем товары из базы по списку уникальных ID
    unique_products = Product.query.filter(Product.id.in_(counts.keys())).all()
    
    products_for_template = []
    total = 0
    
    for product in unique_products:
        quantity = counts[product.id]
        subtotal = product.price * quantity
        total += subtotal
        
        # Собираем данные для отображения
        products_for_template.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'subtotal': subtotal
        })
    
    return render_template('shop/cart.html', products=products_for_template, total=total)

# 3. Оформление заказа (обработка формы)
@shop_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return redirect(url_for('shop.index'))

    # 1. Группируем товары, чтобы посчитать количество каждого
    from collections import Counter
    counts = Counter(cart_ids) # Получаем {id_товара: количество}

    # 2. Считаем общую сумму заказа
    products = Product.query.filter(Product.id.in_(counts.keys())).all()
    total_price = sum(p.price * counts[p.id] for p in products)

    # 3. Создаем запись в таблице orders
    new_order = Order(
        user_id=current_user.id,
        phone=request.form.get('phone'),
        address=request.form.get('address'),
        total_price=total_price,
        status='pending' # или 'Новый'
    )
    db.session.add(new_order)
    db.session.flush() # Получаем ID нового заказа для связи

    # 4. Сохраняем состав заказа в OrderComposition
    for p in products:
        item = OrderComposition(
            order_id=new_order.id,
            product_id=p.id,
            quantity=counts[p.id],      # Сохраняем сколько купили
            price_at_order=p.price      # Фиксируем цену на момент покупки
        )
        db.session.add(item)

    db.session.commit()
    session.pop('cart', None) # Очищаем корзину после успешной записи в БД
    
    return render_template('shop/order_success.html')

@shop_bp.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    if 'cart' in session:
        cart = session['cart']
        if product_id in cart:
            cart.remove(product_id) # Удаляет один экземпляр товара
            session['cart'] = cart
            flash("Товар удален из корзины")
    return redirect(url_for('shop.view_cart'))

@shop_bp.route('/cart/clear')
def clear_cart():
    session.pop('cart', None)
    flash("Корзина очищена")
    return redirect(url_for('shop.view_cart'))