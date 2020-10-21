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
    'kit',
    'link',
]

# values for the bill of material csv file

BILL_HEADERS = [
    'number',
    'title',
    'description',
    'price',
    'quantity',
    'package',
    'seller',
    'kit',
    'link'
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
    # 'kit',
    12: 'link'
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
    # 'kit',
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
    # 'kit',
    12: 'link'
}

# types to assign in the initialization of a popoup editor

TYPES_FROM_EDITOR = ['Jig', 'Project', 'Assembly', 'Assembly', 'Assembly', 'Part', 'Placeholder']

# column sizes of the components page

COMPONENTS_PAGE_SIZES = [150, 200, 340, 130, 130, 130, 340, 60, 60]

# special prefixes used to calculate a number (not needed for now)

SPECIAL_PREFIXES = ['MEH', 'MMH', 'ELH', 'EMH', 'CON']

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

# sections to update when calling update special components

SECTIONS_TO_UPDATE = [2, 3, 4, 5, 6, 8, 10, 11, 13]