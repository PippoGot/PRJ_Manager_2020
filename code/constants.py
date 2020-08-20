# default values of the first node of any project tree

DEFAULT_FIRST_NODE = {
    'number': '#000-000', 
    'parent': '',
    'title': '-', 
    'description': '-',
    'type': 'Project',
    'manufacture': 'Assembled',
    'status': '-',
    'comment':'-',
    'price': 0,
    'quantity': 1,
    'quantityPackage': 1,
    'seller': '-',
    'kit': '-',
    'link': '-'
}

# default headers value

HEADERS = [
    'number', 
    'parent',
    'title', 
    'description',
    'type',
    'manufacture',
    'status',
    'comment',
    'price',
    'quantity',
    'quantityPackage',
    'seller',
    'kit',
    'link'
]

# components types that cant have their manufacture edited

NOT_EDITABLE_TYPES = [
    'Project',
    'Assembly',
    'Hardware',
    'Placeholder',
    'Consumables'
]

# not editable columns of the model

NOT_EDITABLE_COLUMNS = [0, 1, 4]

# columns to show in the hardware list view

COLUMN_LIST_HARDWARE = {
    0: 'number', 
    2: 'name',
    3: 'description',
    4: 'type',
    5: 'manufacture',
    8: 'price',
    10: 'quantityPackage',
    11: 'seller',
    13: 'link'
}

# columns to show in the component tree view

COLUMN_LIST_TREE = {
    0: 'number', 
    2: 'title', 
    3: 'description',
    4: 'type',
    5: 'manufacture',
    6: 'status',
    7: 'comment',
    9: 'quantity',
    11: 'seller',
}

# types to assign in the initialization of a popoup editor

TYPES_FROM_EDITOR = ['Jig', 'Project', 'Assembly', 'Assembly', 'Assembly', 'Part']

# column sizes of the components page

COMPONENTS_PAGE_SIZES = [150, 200, 340, 130, 130, 130, 340, 60, 60]

# column sizes of the hardware editor page

HARDWARE_EDITOR_SIZES = [70, 200, 360, 130, 130, 130, 130, 70, 355]

# special prefixes used to calculate a number (not needed for now)

SPECIAL_PREFIXES = ['MEH', 'MMH', 'ELH', 'EMH', 'CON']

# string list of values for number conversion

VALUES_36_10 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


COLUMNS_TO_UPDATE = [
    'title', 
    'description',
    'type',
    'manufacture',
    'status',
    'price',
    'quantityPackage',
    'seller',
    'link'
]


SECTIONS_TO_UPDATE = [2, 3, 4, 5, 6, 8, 10, 11, 13]