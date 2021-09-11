from odoo import fields, models, api, _, tools
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_price = fields.Float('Product Price', help="Product Price for Eway Bill")
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])
    # cess_non_advol = fields.Integer('CESS Non Advol Amount')
    cess_non_advol = fields.Selection([('0', '0'), ('400', '400'), ('2076', '2076'),
                                       ('2747', '2747'), ('3668', '3668'), ('4006', '4006'),
                                       ('4170', '4170')], string='CESS Non Advol Amount')

    @api.onchange('product_id', 'picking_type_id')
    def onchange_product(self):
        res = super(StockMove, self).onchange_product()
        if self.product_id:
            self.product_price = self.product_id.standard_price
        return res

    def _prepare_procurement_values(self):
        values = super(StockMove, self)._prepare_procurement_values()
        values.update({
            'tax_id': [(6, 0, self.tax_id.ids)],
        })
        return values
