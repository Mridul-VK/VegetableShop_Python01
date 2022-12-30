'''a file with utility functions'''
import json

def list_fetcher(check_list, parameter, value):
    '''returns object based on its property'''
    reqd_item = None
    for item in check_list:
        if item[parameter] == value:
            reqd_item = item
    return reqd_item

def get_data():
    '''a file is being read and returned'''
    file = None
    if file is None:
        with open('./db.json', encoding='utf-8') as json_file:
            file = json.load(json_file)

    products = file['products']
    units = file['units']
    for product in products:
        product_unit = product['unit_id']
        unit = list_fetcher(units, 'unit_id', product_unit)
        product['unit_name'] = unit['unit_name']


    return file

def get_product(param_id=None, name=None):
    '''fetching a particular product'''
    products = get_data()['products']
    if param_id is not None:
        product = list_fetcher(products, 'product_id', param_id)
        return product
    if name is not None:
        product = list_fetcher(products, 'product_name', name)
        return product

    return None

if __name__ == '__main__':
    print(get_product(name='onion'))
