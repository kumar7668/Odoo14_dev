from odoo import models, fields, api, _


class Partner(models.Model):
    _name = "res.partner"
    _inherit = 'res.partner'

    classification_id = fields.Many2one('contact.classification', string='Customer Classification')
    source_ids = fields.Many2many('utm.source', string='Data Origin')
    region_id = fields.Many2one('contact.region', string='Region')
    exhibition_id = fields.Many2one('contact.exhibition', string='Exhibition')
    last_exhibition_id = fields.Many2one('contact.exhibition', string='Last Exhibition')
    book_no = fields.Char('Book No')
    visitor_no = fields.Char('Visitor No')
    customer_code = fields.Char("Customer Code", readonly=True)
    country_id = fields.Many2one('res.country', string='Country',
                                 help="Apply only if delivery country matches.",
                                 track_visibility='onchange')

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        user = self.env.user
        if self.user_has_groups('gts_contact.group_see_own_contacts'):
            self._cr.execute("""select id from res_partner where user_id = %s""" % user.id)
            res = self.env.cr.fetchall()
            partner_ids = [item for t in res for item in t]
            args.append((('id', 'in', partner_ids)))
        return super(Partner, self)._search(args, offset=offset, limit=limit, order=order,
                                            count=count, access_rights_uid=access_rights_uid)

    def create_code(self):
        partner_ids = self.search([('customer_code', '=', False), ('is_company','=',True)])
        count = 1
        for part in partner_ids:
            if part.country_id:
                count += 1
                part.customer_code = part.country_id.code + '/' + '000' + str(part.country_id.next_no)
                part.country_id.next_no += 1
                if count % 300 == 0:
                    self._cr.commit()

    @api.onchange('country_id')
    def fill_region(self):
        for data in self:
            if data.country_id.region_id:
                self.region_id = self.country_id.region_id.id

    def write(self, vals):
        res = super(Partner, self).write(vals)
        country_code = str(self.country_id.code)
        next_no = str(self.country_id.next_no)
        print(country_code)
        print(next_no)
        no = country_code + '/' + '000' + (next_no)
        print(no)
        if vals.get('country_id') and self.is_company:
            self.country_id.next_no += 1
            self.customer_code = no
        return res

    @api.model
    def create(self, vals):
        val = super(Partner, self).create(vals)
        country_code = str(val.country_id.code)
        next_no = str(val.country_id.next_no)
        if val.country_id and val.is_company:
            no = country_code + '/' + '000' + (next_no)
            val.country_id.next_no += 1
            val.customer_code = no
        return val
