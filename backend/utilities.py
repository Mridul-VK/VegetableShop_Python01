'''a file with utility functions'''
import json
import os
import ast

def array_find(array, parameter, value):
    '''returns object based on its property'''
    reqd_item = None
    for item in array:
        if item[parameter] == value:
            reqd_item = item
    return reqd_item


def get_data():
    '''a file is being read and returned'''
    file = None
    if file is None:
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
    data = get_data()

    data['products'] = products
    
    stringified = json.dumps(data['products'], sort_keys=True)
    data['products'] = ast.literal_eval(stringified)

    with open(os.path.abspath('backend/db.json'), 'w', encoding='utf-8') as file:
        json.dump(data, file)

def get_all_products():
    '''fetches all products in db'''
    data = get_data()
    return data['products']


def get_product(product_id=None, product_name=None):
    '''fetching a particular product'''
    products = get_all_products()
    if product_id is not None:
        product = array_find(products, 'product_id', product_id)
        return product
    if product_name is not None:
        product = array_find(products, 'product_name', product_name)
        return product

    return None

def add_product(product, callback):
    '''adds product to products list'''
    product_name = product['product_name']
    price_per_unit = product['price_per_unit']
    stock = product['stock']
    unit_id = product['unit_id']
    if not product_name or not price_per_unit or not stock or not unit_id:
        return None

    products = get_all_products()
    product['product_id'] = len(products) + 1

    for item in products:
        if item['unit_name']:
            del item['unit_name']

    products.append(product)
    save_product(products)
    callback()


if __name__ == '__main__':
    # print(get_product(product_name='onion'))
    product_to_be_added = {
        'product_name': 'pumpkin',
        'price_per_unit': 30,
        'stock': 50,
        'unit_id':2
    }

    def add_callback ():
        '''callback func'''
        print("product added success fully")

    add_product(product_to_be_added, add_callback)
    
