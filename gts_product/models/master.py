from odoo import fields, models

class MasterDetail(models.Model):
    _name = "master.detail"
    _rec_name = 'name'
    name = fields.Char('Name')
    description = fields.Char('Description')

class CustomerTag(models.Model):
    _name = "customer.tag"

    customer_id = fields.Many2one('res.partner', string='Customer')
    product_id = fields.Many2one('product.template', string='Product')
    sku_code = fields.Char('SKU Number')


