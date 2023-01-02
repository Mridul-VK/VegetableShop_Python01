'''a file with utility subfunctions'''
import json
import os
import ast
from general_utility import array_find

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
