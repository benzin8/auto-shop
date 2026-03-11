from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.core.database import db
from app.models.users import User
from app.models.orders import Order
from flask_login import current_user, login_required

from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint('profile', __name__)

@user_bp.route('/profile', methods=['GET'])
@login_required
def check_profile():
    user = db.session.get(User, current_user.id)
    return render_template('auth/profile.html', user=user)

@user_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    
    if not check_password_hash(current_user.password_hash, old_password):
        flash('Старый пароль введен неверно!', 'danger')
        return redirect(url_for('profile.check_profile'))
    
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Пароль успешно обновлен!', 'success')
    return redirect(url_for('profile.check_profile'))

@user_bp.route('/order/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    # Ищем заказ и проверяем, что он принадлежит именно этому пользователю
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != current_user.id:
        abort(403) # Чужой заказ отменить нельзя
        
    # Отменить можно только новый заказ (pending)
    if order.status == 'pending':
        order.status = 'canceled'
        db.session.commit()
        flash(f"Заказ #{order.id} успешно отменен", "info")
    else:
        flash("Этот заказ уже нельзя отменить, так как он находится в обработке", "warning")
        
    return redirect(url_for('profile.check_profile'))