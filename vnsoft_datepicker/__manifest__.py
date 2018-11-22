# -*- coding: utf-8 -*-

{
    'name': 'vnsoft_datepicker',
    'version': '0.1',
    'category': 'hide',
    'sequence': 20,
    'summary': 'Tools',
    'description': """
增加日历选择插件功能，可以限制日期选择范围
==========================================

    """,
    'author': 'VnSoft',
    'website': 'https://www.odoo.com/page/crm',
    # 'images': ['images/Sale_order_line_to_invoice.jpeg','images/sale_order.jpeg','images/sales_analysis.jpeg'],
    'depends': ['web'],
    'data': ["datepicker.xml"],
    "qweb":[],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}