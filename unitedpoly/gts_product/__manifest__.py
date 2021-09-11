# -*- encoding: utf-8 -*-
{
    'name': 'gts_product',
    'version': '14.0.0.1',
    'category': 'Product',
    'summary': 'Product form',
    'sequence': 1,
    'author': 'Geo Technosoft',
    'website': 'http://www.geotechnosoft.com',
    'depends': ['product', 'stock', 'sale', 'purchase', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/product_product.xml',
        'views/master.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
}
