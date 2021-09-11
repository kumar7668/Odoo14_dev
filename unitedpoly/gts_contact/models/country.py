from odoo import models, fields, api, _


class ResCountry(models.Model):
    _inherit = 'res.country'

    region_id = fields.Many2one('contact.region', string='Country Region')
    next_no = fields.Integer("Next NO", default=1)
