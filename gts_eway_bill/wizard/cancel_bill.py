import json

from odoo import fields, models, _
from odoo.exceptions import UserError


class EbillCancel(models.TransientModel):
    _name = 'ebill.cancel'

    # reason = fields.Selection([('1', 'Due To Break Down'),
    #                            ('2', 'Due To Transhipment'),
    #                            ('3', 'Others'),
    #                            ('4', 'First time'), ], string='Reason')
    reason = fields.Selection([('1', 'Duplicate'),
                               ('2', 'Order Cancelled'),
                               ('3', 'Data Entry mistake'),
                               ('4', 'Others'), ], string='Reason')
    remark = fields.Text('Remark')

    def cancel_bill(self):
        active_id = self.env.context.get('active_id')
        order = self.env['stock.picking'].browse(active_id)
        if order.cancel_date:
            raise UserError(_('This Bill is already Cancelled'))
        if not order.ewaybill_no:
            raise UserError(_('Eway Bill No Not Exits'))
        cancel_dic = {
            'ewbNo': order.ewaybill_no,
            'cancelRsnCode': self.reason,
            'cancelRmrk': self.remark
        }
        configuration = self.env['eway.configuration'].search([])
        data_base64 = json.dumps(cancel_dic)
        response = configuration.generate_eway(data_base64, 'CANEWB')
        if response and response.status_code == 200:
            order.cancel_date = (response.json().get('cancelDate'))
            order.bill_status = 'cancel'
        else:
            raise UserError(_(response.text))
