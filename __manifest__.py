# -*- coding: utf-8 -*-
{
    'name': "addons/material_module",
    'summary': "module for managing material",
    'description': "module for managing material",
    'author': "Galang Ardian",
    'website': "https://www.github.com/neuthos",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'test': [
        'tests/test_material.py',
    ],
}
