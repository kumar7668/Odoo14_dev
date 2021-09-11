# from odoo import models, fields
#
# class ResUser(models.Model):
#     _inherit = 'res.users'
#
#     user_email_lines = fields.One2many('res.data', 'email_id', string="User Email ")
#
#
#
# class ResData(models.Model):
#     _name = 'res.data'
#     _description = "User Data"
#
#     user_id = fields.Many2one('res.users', string="User Id")
#     email_id = fields.Many2one("res.company", string="Email Id")
#     company_id = fields.Many2one("res.company", string=" Company Id")
