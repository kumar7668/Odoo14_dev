from odoo import api, models, fields, _
from odoo.exceptions import UserError
import math


class Partner(models.Model):

    _inherit = 'res.partner'

    # customer_code=fields.Char("Customer Code",readonly=True)
    country_id = fields.Many2one('res.country', string='Country',
                                 help="Apply only if delivery country matches.",track_visibility='onchange')

    # def write(self,vals):
    #     res = super(Partner, self).write(vals)
    #     country_code = str(self.country_id.code)
    #     next_no = str(self.country_id.next_no)
    #     print(country_code)
    #     print(next_no)
    #     no = country_code + '/' + '000' + (next_no)
    #     print(no)
    #     if vals.get('country_id'):
    #         self.country_id.next_no += 1
    #         self.customer_code = no
    #     return res

    # @api.model
    # def create(self, vals):
    #     val=super(Partner,self).create(vals)
    #     country_code = str(val.country_id.code)
    #     next_no = str(val.country_id.next_no)
    #     if val.country_id:
    #         no = country_code + '/' + '000' + (next_no)
    #         val.country_id.next_no += 1
    #         val.customer_code = no
    #     else:
    #         val.customer_code=""
    #     return val


class Country(models.Model):

    _inherit = 'res.country'

    next_no = fields.Integer("Next NO", default=1)

    # @api.depends('country_id')
    # def update(self):
    # if
    #     self.country_id.next_no +=1
