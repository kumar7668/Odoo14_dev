from odoo import models, fields

class VaccinesVaccines(models.Model):
    _name ='vaccine.vaccine'

    v_name = fields.Char(string='Vaccine Name', required=True)
    v_photo  = fields.Binary(string='Product Image')