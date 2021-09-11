from odoo import api, models, fields, _
from odoo.exceptions import UserError
import math
from num2words import num2words


class AccountMove(models.Model):
    _inherit = 'account.move'

    vessel_no = fields.Char(string="Vessel No")
    place_of_delivery = fields.Char(string="Place of Delivery")
    port_of_discharge = fields.Char(string="Port of Discharge")
    port_of_loading = fields.Char(string="Port of Loading")
    pre_carriege_by = fields.Char(string="Pre Carriege By")
    no_pkg = fields.Char(string="No of Pkg.")
    net_weight = fields.Float('Net Weight')
    gross_weight = fields.Float('Gross Weight')
    volume = fields.Float('Volume/CBM')
    shipping_term = fields.Selection([('fob','FOB'),('cif','CIF'),('dap','DAP')], string='Shipping Terms')
    freight_charge = fields.Float("Freight Charge")
    insurance_charge = fields.Float("Insurance Charge")

    def num_to_word(self):
        total = self.amount_total + self.freight_charge + self.insurance_charge
        num_word = num2words(total)
        num_word_upper = num_word.upper()
        return num_word_upper

    def get_product_categories(self, o):
        category_list = []
        for line in o.invoice_line_ids:
            category_list.append(line.product_id.categ_id.parent_id.id)
        category_list = list(set(category_list))
        return self.env['product.category'].browse(category_list)

    def get_so_lines_category_wise(self, o, category):
        return o.invoice_line_ids.filtered(lambda sol: sol.product_id.categ_id.parent_id.id == category.id)


class MoveLine(models.Model):
    _inherit = 'account.move.line'

    item_code = fields.Char('Party Item Code')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    vessel_no = fields.Char(string="Vessel No")
    place_of_delivery = fields.Char(string="Place of Delivery")
    port_of_discharge = fields.Char(string="Port of Discharge")
    port_of_loading = fields.Char(string="Port of Loading")
    pre_carriege_by = fields.Char(string="Pre Carriege By")
    no_pkg = fields.Char(string="No of Pkg.")
    net_weight = fields.Float('Net Weight')
    gross_weight = fields.Float('Gross Weight')
    volume = fields.Float('Volume/CBM')
    shipping_term = fields.Selection([('fob', 'FOB'), ('cif', 'CIF'), ('dap', 'DAP')], string='Shipping Terms')
    term_of_delivery=fields.Char(string="Term of Delivery")
    shipment_mode = fields.Char(string="Shipment Mode")
    freight_charge=fields.Float("Freight Charge")
    insurance_charge=fields.Float("Insurance Charge")

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['vessel_no'] = self.vessel_no
        invoice_vals['place_of_delivery'] = self.place_of_delivery
        invoice_vals['port_of_discharge'] = self.port_of_discharge
        invoice_vals['port_of_loading'] = self.port_of_loading
        invoice_vals['pre_carriege_by'] = self.pre_carriege_by
        invoice_vals['no_pkg'] = self.no_pkg
        invoice_vals['net_weight'] = self.net_weight
        invoice_vals['gross_weight'] = self.gross_weight
        invoice_vals['volume'] = self.volume
        invoice_vals['shipping_term'] = self.shipping_term
        invoice_vals['freight_charge'] = self.freight_charge
        invoice_vals['insurance_charge'] = self.insurance_charge
        return invoice_vals

    def num_to_word(self):
        total = self.amount_total + self.freight_charge + self.insurance_charge
        num_word = num2words(total)
        num_word_upper = num_word.upper()
        return num_word_upper

    def get_product_categories(self, doc):
        category_list = []
        for line in doc.order_line:
            category_list.append(line.product_id.categ_id.parent_id.id)
        category_list = list(set(category_list))
        return self.env['product.category'].browse(category_list)

    def get_so_lines_category_wise(self, doc, category):
        return doc.order_line.filtered(lambda sol: sol.product_id.categ_id.parent_id.id == category.id)


class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    item_code = fields.Char('Party Item Code')
