'''server'''
from flask import Flask, request
from all_utility.mainfunctions import get_all_products, add_product, add_units, delete_product, edit_product, get_product, get_units

app = Flask(__name__)

@app.route("/api/get_all_products")
def s_get_all_products():
    '''gets all products'''
    return get_all_products()

@app.route("/api/get_product/<int:product_id>")
def s_get_product(product_id):
    '''gets a given product'''
    return get_product(product_id)

@app.route("/api/add_product", methods=["POST"])
def s_add_product():
    '''adds a product in inventory'''
    product_name, stock, price_per_unit, unit_id = request.form
    product = {product_name, stock, price_per_unit, unit_id}
    return add_product(product)

@app.route("/api/edit_product", methods = ["POST"])
def s_edit_product():
    '''edits a given product'''
    product_id, price_per_unit, stock, stock_type = request.form
    return edit_product(product_id, {stock, price_per_unit}, stock_type)


if __name__ == '__main__':
    app.run(debug=True,port=7104)