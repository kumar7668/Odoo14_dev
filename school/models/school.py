from odoo import models, fields

class SchoolRole(models.Model):
    _name = "school.role"

    name = fields.Char(string="School Name")
    email = fields.Char(string="Email")
    phone_no = fields.Char("Phone Num")









    



