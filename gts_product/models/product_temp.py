from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    noun_name1 = fields.Char("Noun Name1")
    noun_name2 = fields.Char("Noun Name2")
    noun_name3 = fields.Char("Noun Name3")
    noun_name4 = fields.Char("Noun Name4")
    make_id = fields.Many2one('master.detail', string='Make')
    part_Number = fields.Char("Part Number")
    customer_tag_line = fields.One2many('customer.tag', 'product_id', string='Customer Tags')
    country_origin = fields.Many2one('res.country', string="Country Origin")

