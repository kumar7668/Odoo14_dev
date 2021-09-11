# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
import math

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import AccessError, UserError
from odoo.tools import float_compare


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, values):
        if 'raw_material_production_id' in values:
            browse_id = self.env['mrp.production'].browse(values['raw_material_production_id'])
            if 'product_uom_qty' in values:
                if browse_id.product_qty > 0.0:
                    values['unit_factor'] = values['product_uom_qty'] / browse_id.product_qty
                    print(values['unit_factor'], "**********************8")
        production = super(StockMove, self).create(values)
        return production



    def write(self, values):
        if self.raw_material_production_id and 'product_uom_qty' in values:
            if self.raw_material_production_id.product_qty > 0.0:
                values['unit_factor'] = self.product_uom_qty / self.raw_material_production_id.product_qty
                print(values['unit_factor'], "********************")
        return super(StockMove, self).write(values)








