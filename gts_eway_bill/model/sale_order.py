from odoo import fields, models, api, _, tools
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
        values.update({
            'tax_id': [(6, 0, self.tax_id.ids)],
        })
        return values
