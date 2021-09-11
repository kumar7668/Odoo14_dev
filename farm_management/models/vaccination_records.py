from odoo import models, fields

class VaccinationRecordsVaccinationRecords(models.Model):
    _name ='vaccinationrecord.vaccinationrecord'
    _inherits={'farmanimal.farmanimal','vaccine.vaccine'}

    vaccinated_animal =  fields.Many2one( 'farmanimal.farmanimal', string='Vacinated Animal',)
    vaccine_name = fields.Many2many('vaccine.vaccine', related='v_name', string='Vaccine(s)',)
    vaccination_date_time = fields.Datetime(string='Date and Time',default=fields.Datetime.now,)
    next_vaccination_date = fields.Date(string='Next Date',)