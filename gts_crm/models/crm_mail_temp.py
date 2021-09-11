from odoo import fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def write(self, values):
        res = super(CrmLead, self).write(values)
        if values.get('user_id'):
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('crm.crm_lead_action_pipeline').id
            params = str(base_url) +"/web#id=%s&view_type=form&model=crm.lead&action=%s" % (self.id, action_id)
            cr_url = str(params)
            template = self.env.ref('gts_crm.mail_template_crm_lead')
            if template:
                values = template.generate_email(self.id,
                                                 ['subject', 'email_to', 'email_from', 'body_html'])
                values['body_html'] = values['body_html'].replace('_cr_url', cr_url)
                print(cr_url)
                mail = self.env['mail.mail'].create(values)
                try:
                    mail.send()
                except Exception:
                    pass
        return res








