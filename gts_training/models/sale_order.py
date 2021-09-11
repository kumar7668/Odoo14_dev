from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char('Custom Field')

    name_d = fields.Char('Deepak')

    def start_button(self):
        pass

