# -*- coding: utf-8 -*-
{
    'name': 'AdminLTE Backend Theme',
    "summary": "Odoo 10.0 community adminlte backend theme",
    'category': 'Themes/Backend',
    'author': '675938238@qq.com',
    'version': '10.0.1.0.0',
    'description': '',
    'depends': ['web'],
    'data': [
        'views/assets.xml',
        'views/webclient_templates.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
    ],
    'auto_install': False

}
