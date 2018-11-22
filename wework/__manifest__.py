# -*- coding: utf-8 -*-
{
    'name': "企业微信",

    'summary': """
        企业微信""",

    'description': """
        企业微信
    """,

    'author': "DingYii",
    'website': "http://www.dingyii.cn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'views/views.xml',
        #'views/hr.xml',
        #'views/templates.xml',
        #'views/res_config.xml',
        #'views/multi_actions.xml',
        #'views/actions.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable':True,
    'application':True,
    'auto_install':False,
}