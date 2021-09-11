from odoo import models, fields

class ResUser(models.Model):
    _inherit = 'res.users'

    user_email_ids = fields.One2many('user.email.line', 'user_id', string="User Data ")


class UserEamilLine(models.Model):
    _name = 'user.email.line'

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.name)
    company_name_id = fields.Many2one( 'res.company', string='Company Name')
    email_id = fields.Char(string='Email Id')








