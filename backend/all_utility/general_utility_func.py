'''a file with utility functions'''

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
