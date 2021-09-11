from odoo import models, fields


class Salary(models.Model):
    _name = 'salary.salary'
    _rec_name = 'description'

    name = fields.Char('Name')
    description = fields.Char('Description')
    details_ids = fields.One2many('geo.tech', 'salary_id', 'Details')
    date = fields.Date('Date')
