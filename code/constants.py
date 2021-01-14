# default headers value

HEADERS = [
    'number',
    'title',
    'description',
    'type',
    'manufacture',
    'status',
    'comment',
    'price',
    'quantity',
    'package',
    'seller',
    'link',
]

# columns to show in the hardware list view

COLUMN_LIST_HARDWARE = {
    0: 'number',
    1: 'title',
    2: 'description',
    3: 'type',
    4: 'manufacture',
    # 'status',
    # 'comment',
    7: 'price',
    # 'quantity',
    9: 'package',
    10: 'seller',
    11: 'link'
}

# columns to show in the component tree view

COLUMN_LIST_TREE = {
    0: 'number',
    1: 'title',
    2: 'description',
    3: 'type',
    4: 'manufacture',
    5: 'status',
    6: 'comment',
    # 'price',
    8: 'quantity',
    # 'package',
    10: 'seller'
    # 'link',
}

# columns to show in the bill page

COLUMN_LIST_BILL = {
    0: 'number',
    1: 'title',
    2: 'description',
    # 'type',
    # 'manufacture',
    # 'status',
    # 'comment',
    7: 'price',
    8: 'quantity',
    9: 'package',
    10: 'seller',
    11: 'link'
}

# column sizes of the components page

COMPONENTS_PAGE_SIZES = [150, 200, 340, 130, 130, 130, 340, 60, 60]

# columns to update when calling update special components

COLUMNS_TO_UPDATE = [
    'title',
    'description',
    'type',
    'manufacture',
    'status',
    'price',
    'package',
    'seller',
    'link'
]
