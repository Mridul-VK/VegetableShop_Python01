'''a file with utility functions'''
import json
import os
import ast

# ========================================================
# Helper default functions
# ========================================================


def array_find(array, parameter, value):
    '''returns object based on its property'''
    reqd_item = None
    for item in array:
        if item[parameter] == value:
            reqd_item = item
    return reqd_item


def array_filter(array, parameter, value):
    '''filters a given array'''
    reqd_array = []
    for item in array:
        if item[parameter] != value:
            reqd_array.append(item)

    return reqd_array

# ========================================================
# Helper sub-functions
# ========================================================


def get_data():
    '''a file is being read and returned'''
    file = None
    if file is None:
        try:
            with open(os.path.abspath('backend/db.json'), encoding='utf-8') as json_file:
                file = json.load(json_file)
        except FileNotFoundError:
            with open(os.path.abspath('backend/db.json'), 'w', encoding='utf-8') as json_file:
                json.dump({'products': [], 'units': []}, json_file, indent=2)
            with open(os.path.abspath('backend/db.json'), encoding='utf-8') as json_file:
                file = json.load(json_file)

    products = file['products']
    units = file['units']
    for product in products:
        product_unit = product['unit_id']
        unit = array_find(units, 'unit_id', product_unit)
        product['unit_name'] = unit['unit_name']

    return file


def save_product(products):
    '''adds products to db'''
    for item in products:
        if 'unit_name' in item:
            del item['unit_name']

    data = get_data()

    data['products'] = products

    stringified = json.dumps(data['products'], sort_keys=True)
    data['products'] = ast.literal_eval(stringified)

    with open(os.path.abspath('backend/db.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


# ========================================================
# Export functions
# ========================================================

def get_all_products():
    '''fetches all products in db'''
    data = get_data()
    return data['products']


def get_product(product_id):
    '''fetching a particular product'''
    products = get_all_products()
    if product_id is not None:
        product = array_find(products, 'product_id', product_id)
        return product

    return 'Product not found!'


def add_product(product):
    '''adds product to products list'''
    product_name = product['product_name']
    price_per_unit = product['price_per_unit']
    stock = product['stock']
    unit_id = product['unit_id']
    if not product_name or not price_per_unit or not stock or not unit_id:
        return 'product_name, price_per_unit, stock and unit_id are required properties of product!'

    products = get_all_products()
    product['product_id'] = len(products) + 1

    product_exist = array_find(products, 'product_name', product_name)
    if product_exist is not None:
        return 'Product already exists. Please use edit method to edit the product!'

    products.append(product)
    save_product(products)
    return 'Product added successfully'


def add_units(unit_name):
    '''adds new unit system to db'''
    if not unit_name:
        return 'unit_name is required'

    data = get_data()
    new_unit = {
        'unit_id': len(data['units']) + 1,
        'unit_name': unit_name
    }

    data['units'].append(new_unit)

    with open(os.path.abspath('backend/db.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)

    return 'New unit added successfully'


def edit_product(product_id, update_data, stock_type='inc'):
    '''edits product from db'''
    if not product_id or not isinstance(product_id, int):
        return 'Product id is required parameter'

    price_per_unit = None
    stock = None

    if 'price_per_unit' in update_data:
        price_per_unit = update_data['price_per_unit']
    if 'stock' in update_data:
        stock = update_data['stock']

    if not price_per_unit and not stock:
        return 'Required parameters: price_per_unit &/or stock are missing'

    product = get_product(product_id)

    if not product:
        return 'Product not found'

    if price_per_unit is not None:
        product['price_per_unit'] = price_per_unit

    if stock is not None:
        match stock_type:
            case 'inc':
                product['stock'] += stock
            case 'dec':
                product['stock'] -= stock
            case 'exact':
                product['stock'] = stock
            case _:
                return 'Command not recognised'

    products = get_all_products()
    products[product_id-1] = product
    save_product(products)
    return 'Product was edited successfully!'


def delete_product(product_id):
    '''deletes product from db'''
    if not product_id or not isinstance(product_id, int):
        return 'product_id is a required parameter'

    products = get_all_products()
    if product_id > len(products):
        return 'Product not found!'

    products = array_filter(products, 'product_id', product_id)

    for index, item in enumerate(products, 1):
        item['product_id'] = index

    save_product(products)

    return 'Product was successfully removed from the inventory!'


if __name__ == '__main__':
    RESULT = get_data()
    print(RESULT)
