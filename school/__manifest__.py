{
    'name': "School",
    'summary': """ School Management System """,
    'description': """ This is a School Data Management Tool supported in odoo14.   """,
    'author': "Geotechnosoft",
    'website': "https://www.geotechnosoft.com",
    'category': 'School',
    'version': '14.0.0',
    'depends': ['base',],
    'data': [
        'security/ir.model.access.csv',
        'views/school_view.xml'

    ],
}
