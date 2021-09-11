from odoo import models, fields, api, _


class ContactClassification(models.Model):
    _name = 'contact.classification'
    _description = 'Classification'
    _rec_name = 'name'

    name = fields.Char(string='Name')


class ContactRegion(models.Model):
    _name = 'contact.region'
    _description = 'Region'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')


class ContactExhibition(models.Model):
    _name = 'contact.exhibition'
    _description = 'Exhibition'
    _rec_name = 'name'

    name = fields.Char('Name')


class ContactLastExhibition(models.Model):
    _name = 'contact.last.exhibition'
    _description = 'Last Exhibition'
    _rec_name = 'name'

    name = fields.Char('Name')
