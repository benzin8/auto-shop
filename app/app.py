from app.core.factory import create_app
from flask import render_template
from app.models.products import Product
app = create_app()

@app.route('/')
def root():
    all_products = Product.query.all() 
    return render_template('main_page.html', products=all_products)

