from odoo import models, fields, api, _


class Product(models.Model):
    _inherit = 'product.template'

    upl_code_id = fields.Many2one('product.upl.code', string='UPL Code')
    upl_subcode_id = fields.Many2one('product.upl.subcode', string='UPL Code')
    material_id = fields.Many2one('product.material', string='UPL Code')
    size = fields.Char(string='Size')
    thickness = fields.Char(string='Thickness')
    primary_packaging = fields.Char(string='Primary Packaging')
    no_of_units_per_pack = fields.Char(string='No of Unit Per Pack')
    secondary_packing = fields.Char(string='Secondary Packing')
    no_of_units_per_secondary_pack = fields.Char(string='No of Units Per Secondary Packing')
    primary_packaging_dimension = fields.Char(string='Primary Packaging Dimension')
    volume = fields.Char(string='Volume')
    height = fields.Char(string='Height')
    secondary_packaging_dimension = fields.Char(string='Secondary Packaging Dimension')
    secondary_volume = fields.Char(string='Volume')
    secondary_height = fields.Char(string='Height')
    no_of_unit_per_carton = fields.Char(string='No of Unit Per Carton')
    net_weight = fields.Float(string='Net Weight')
    finish = fields.Selection([
        ('B', 'Bright'),
        ('F', 'Finish'),
    ], string='Finish')