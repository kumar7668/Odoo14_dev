from odoo import models, fields

class FeedRecordsFeedRecords(models.Model):
    _name ='feedrecord.feedrecord'
    _inherits={'farmanimal.farmanimal','feed.feed'}

    feed_animal =  fields.Many2one( 'farmanimal.farmanimal', string='Feed Animal',)
    feed_name = fields.Many2many('feed.feed', related='f_name', string='Consumed Feed(s)',)
    amount  = fields.Integer(string='Amount(In Grams)',)
    feed_date_time = fields.Datetime(string='Date and Time',default=fields.Datetime.now,)
    
    
    