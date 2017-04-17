# -*- coding: utf-8 -*-
{
    'name': 'Survey for Task',
    'version': '10.0.1.0.0',
    'author': 'Contractor Andrey S. 2017',
    'category': 'Marketing',
    'description': """
Survey for Task
===============
Survey for Task
    """,
    'depends': [
        'product',
        'project',
        'survey',
        'sale_timesheet',
    ],
    'data': [
        'views/product_template_views.xml',
        'views/project_task_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
