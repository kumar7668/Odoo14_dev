from odoo import fields, models
from odoo import api
class SponsorDetail(models.Model):
    _name = "sponsor.detail"
    _rec_name = 'sponsor_id'
    _description = 'Sponsor Details'

    _inherit = ['mail.thread', 'mail.activity.mixin']

    sponsor_id = fields.Many2one('res.partner', string='Sponsor Name',required=True)
    order_id = fields.Many2one('sale.order', string='Order')
    invoice_id = fields.Many2one('account.move', string='Invoice')
    amount_received = fields.Float(string='Amount Received')
    amount_declared = fields.Float(string='Amount Declared')
    amount_paid = fields.Float(string='Amount Paid')
    payment_id = fields.Many2one('account.payment', string='Payment')
    date = fields.Date('Date')
    customer_company_name_id = fields.Many2one('res.partner', string='Customer Company', required=True,)

    expiry_date = fields.Date(string='Expiry Date')






    #
    # @api.onchange('customer_company_name_id')
    # def onchange_customer_company_name_id(self):
    #     for rec in self:
    #         return {'domain': {'order_id': [('partner_id', '=', rec.customer_company_name_id.id)]}}
    #






