from odoo import models, fields

class FeedsFeeds(models.Model):
    _name ='feed.feed'

    f_name = fields.Char(string='Feed Name', required=True)
    f_photo  = fields.Binary(string='Product Image')