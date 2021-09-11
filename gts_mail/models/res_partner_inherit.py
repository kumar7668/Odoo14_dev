from odoo import api, models, fields, tools

class Partner(models.Model):
    _inherit ="res.partner"

    @api.depends('name', 'email')
    def _compute_email_formatted(self):
        for partner in self:
            user = partner.env.user
            if user.user_email_ids:
                for data in user.user_email_ids:
                    if data.company_name_id.id == partner.env.company.id:
                        partner.email_formatted = data.email_id
            else:
                if partner.email:
                    partner.email_formatted = tools.formataddr((partner.name or u"False", partner.email or u"False"))
                else:
                    partner.email_formatted = ''

