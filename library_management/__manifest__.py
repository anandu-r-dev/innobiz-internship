{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Education',
    'summary': 'Manage books and library records',
    'description': 'Module for managing books.',
    'author': 'Sahala Rezak',
    'depends': ['base'],
    'data': [
         'security/library_security.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
    ],
    'installable': True,
    'application': True,
}