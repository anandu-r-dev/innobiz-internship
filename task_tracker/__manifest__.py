{
    'name': 'Task Tracker',
    'version': '1.2',
    'author': 'Shahanas',
    'category': 'Tools',
    'summary': 'Track and manage tasks',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/task_tracker_groups.xml',
        'views/task_views.xml',
       
    ],
    'installable': True,
    'application': True,
}