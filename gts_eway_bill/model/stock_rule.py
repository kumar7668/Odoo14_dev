from odoo import models, api, _
from odoo.exceptions import UserError

from collections import namedtuple, OrderedDict, defaultdict


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_custom_move_fields(self):
        fields = super(StockRule, self)._get_custom_move_fields()
        fields += ['tax_id',]
        return fields

    def _push_prepare_move_copy_values(self, move_to_copy, new_date):
        new_move_vals = super(StockRule, self)._push_prepare_move_copy_values(
            move_to_copy, new_date)
        new_move_vals.update({
            'tax_id': [(6, 0, move_to_copy.tax_id.ids)],
        })
        return new_move_vals
