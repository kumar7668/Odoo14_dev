from odoo import models, fields

class DiseasesDiseases(models.Model):
    _name ='disease.disease'
    _inherits='vaccine.vaccine'

    d_name= fields.Char(string='Name', required=True)
    d_type = fields.Selection(
        [('infectious disease','Infectious Disease'), ('deficiency','Deficiency'), ('hereditary','Hereditary'), ('physiological','Physiological')], string='Disease Type')
    s_vector = fields.Selection(
        [('airborne','Airborne'), ('foodborne','Foodborne'), ('infectious','Infectious'), ('lifestyle','Lifestyle'), ('non-communicable','Non-communicable')], 
        string='Spread Vector')
    threat_level = fields.Selection(
        [('high','High'), ('medium','Medium'), ('low','Low'), ('quarantine','Quarantine')], string='Threat Level')
    cure = fields.Many2many('vaccine.vaccine', related='v_name', string='Cure')
    
    