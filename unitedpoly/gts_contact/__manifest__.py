{
    "name": " GTS Contact",
    "sequence": "1",
    "summary": " Add Sequence No Accpording to Country Code",
    "version": "14.0.1.0.1",
    "category": "email",
    "author": "TECHNOGEO SOFT Pvt. Ltd.",
    "website": "http://www.geotechnosoft.com",
    "description": """

        """,
    "license": "LGPL-3",
    "installable": True,
    "depends": ['base', 'contacts'],
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/contact.xml',
        'views/country.xml',
        'views/master.xml',
    ],
}
