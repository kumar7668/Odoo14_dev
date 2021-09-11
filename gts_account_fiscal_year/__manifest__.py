# -*- encoding: utf-8 -*-
{
    'name': 'GTS Account Fiscal Year',
    'version': '13.0.0.1',
    'category': 'Accounting',
    'summary': 'Fiscal year and account period creation',
    'description': """
        This module provide feature to define accounting fiscal year and period for company 
        and link with journal entry odoo
        Account fiscal year in odoo 13 Account fiscal period in odoo 13
        Account fiscal period odoo accounting fiscal period form view tree view odoo
        account period odoo
    """,
    'sequence': 1,
    'author': 'Geo Technosoft',
    'website': 'http://www.geotechnosoft.com',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_fiscal_year_view.xml',
        'views/account_move_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'price': 19.99,
    'currency':'EUR',
    'license': 'OPL-1',
    'installable': True,
    'application': True,
}
