from odoo import models, fields, api, _


# class ProductUplcode(models.Model):
#     _name = 'product.upl.code'
#     _rec_name = 'name'
#
#     name = fields.Char(string='Name')
#     code = fields.Char(string='Name')
#
#
# class ProductUplSubcode(models.Model):
#     _name = 'product.upl.subcode'
#     _rec_name = 'name'

    # name = fields.Char(string='Name')


class ProductMaterial(models.Model):
    _name = 'product.material'
    _rec_name = 'name'

    name = fields.Char(string='Name')
