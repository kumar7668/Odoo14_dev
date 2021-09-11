from odoo import models, fields, api, _


class CreateSponsor(models.TransientModel):
    _name = 'create.sponsor'

    sponsor_id = fields.Many2one('res.partner', string='Sponsor Name')
    date = fields.Date('Date')


    def create_sponsor_record(self):
        pass
