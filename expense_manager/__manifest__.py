{
    'name': 'Expense Manager',
    'version': '1.3',
    'author': 'Nihala P A',
    'depends': ['base','web'],
    'data': [
    'security/security.xml',
    'security/ir.model.access.csv',
    'views/expense_record_views.xml',
    'report/expense_report.xml',

],
    'installable': True,
    'application': True,
}