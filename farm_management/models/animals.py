from odoo import models, fields

class FarmAnimalsFarmAnimals(models.Model):
    _name ='farmanimal.farmanimal'

    name= fields.Char(string='Name', required=True)
    photo = fields.Binary(string='Image')
    sex = fields.Selection([('male','Male'),('female','Female')], string='Sex')
    animal_dob = fields.Date(string='Date of birth/entry')
    animal_type = fields.Selection(
        [('cow','Cow'), ('bull','Bull'), ('goat','Goat'), ('sheep','Sheep'), 
        ('fish','Fish'), ('rabbit','Rabbit'), ('chicken','Chicken'), ('turkey','Turkey'),
        ('ducks','Ducks'),('quells','Quells'),('camel','Camel'), ('horse','Horse'),], 
        string='Animal Type') 