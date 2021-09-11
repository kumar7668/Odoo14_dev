from odoo import models, fields, api, _


class Product(models.Model):
    _inherit = 'product.product'


    # upl_code = fields.Char(string='UPL Code')
    # upl_subcode = fields.Char(string='UPL SubCode')
    # material_id = fields.Many2one('product.material', string='Material')
    # size = fields.Char(string='Size')
    # thickness = fields.Char(string='Thickness')
    # master_packaging = fields.Char(string='Master Packaging')
    # no_of_units_per_master_pack = fields.Char(string='No of units per Master packing')
    # secondary_packing = fields.Char(string='Secondary Packaging')
    # no_of_units_per_secondary_pack = fields.Char(string='No of units per secondary packing')
    # # primary_packaging_dimension = fields.Char(string='Primary Packaging Dimension')
    # master_volume = fields.Float(string='Volume')
    # height = fields.Float(string='Height')
    # length = fields.Float(string='Length')
    # width = fields.Float(string='Width')
    # master_weight = fields.Float(string='Weight')
    # # secondary_packaging_dimension = fields.Char(string='Secondary Packaging Dimension')
    # secondary_volume = fields.Float(string='Volume')
    # secondary_height = fields.Float(string='Height')
    # secondary_length = fields.Float(string='Length')
    # secondary_width = fields.Float(string='Width')
    # secondary_weight = fields.Float(string='Weight')
    # # no_of_unit_per_carton = fields.Char(string='No of Unit Per Carton')
