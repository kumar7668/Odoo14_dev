{
    'name': 'Farm Management',
    'version':'12.0.1.0.0',
    'summary':'Record and manage farm Information',
    'category':'Tools',
    'author':'Tumukunde Arnold',
    'maintainer': 'ADD Consultancy',
    'company':'ADD Consultancy',
    'website':'https://www.add.ug',
    'depends':['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/farm_view.xml',
        'views/diseases_view.xml',
        'views/feed_records_view.xml',
        'views/feeds_view.xml',
        'views/vaccination_records_view.xml',
        'views/vaccines_view.xml',
    ],
    'images':[],
    'license':'AGPL-3',
    'installable':True,
    'application':False,
    'auto_install':False,
}