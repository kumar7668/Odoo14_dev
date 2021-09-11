import json
import logging
from datetime import datetime
import requests
import base64

from odoo import fields, models, api, _, tools
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

_logger = logging.getLogger(__name__)


def geo_query_address(street=None, zip=None, city=None, state=None, country=None):
    if country and ',' in country and (country.endswith(' of') or country.endswith(' of the')):
        # put country qualifier in front, otherwise GMap gives wrong results,
        # e.g. 'Congo, Democratic Republic of the' => 'Democratic Republic of the Congo'
        country = '{1} {0}'.format(*country.split(',', 1))
    return tools.ustr(', '.join(filter(None, [street, ("%s %s" % (zip or '', city or '')).strip(), state, country])))


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    generate_ewaybill = fields.Boolean("E-Way Bill?", help='Generate E-way Bill?')
    supply_type = fields.Selection([('I', 'Inward'),
                                    ('O', 'Outward')], string="Supply Type", tracking=2)
    vehicle_type = fields.Selection([('R', 'Regular'),
                                     ('O', 'ODC')], string="Vechicle Type", tracking=2)
    sub_supply_type = fields.Selection([('1', 'Supply'),
                                        ('2', 'Import'),
                                        ('3', 'Export'),
                                        ('4', 'Job Work'),
                                        ('5', 'For Own Use'),
                                        ('6', 'Job Work Return'),
                                        ('7', 'Sale Return'),
                                        ('8', 'Other'),
                                        ('9', 'SKD/CDK'),
                                        ('10', 'Line Sales'),
                                        ('11', 'Recipient Not Known'),
                                        ('12', 'Exhibiation or Fairs'),
                                        ], string="Sub Supply Type", copy=False, tracking=2)
    transportation_mode = fields.Selection([('1', 'Road'),
                                            ('2', 'Rail'),
                                            ('3', 'Air'),
                                            ('4', 'Ship'),
                                            ], string="Transportation Mode", copy=False, tracking=2)
    transporter_id = fields.Many2one('res.partner', string="Transporter", tracking=2)
    transportation_distance = fields.Integer("Distance(Km)", tracking=2,
                                           help='If entered, we will use this distance')
    trans_id = fields.Char("Transporter ID", tracking=2)
    ewaybill_no = fields.Char("E-way Bill No", copy=False, tracking=2)
    vehicle_no = fields.Char("Vehicle No", tracking=2)
    document_type = fields.Selection([('INV', 'Tax Invoice'),
                                      ('BIL', 'Bill of Supply'),
                                      ('BOE', 'Bill of Entry'),
                                      ('CHL', 'Delivery Challan'),
                                      ('OTH', 'Others')], string="Document Type", copy=False,
                                     tracking=2)
    doc_date = fields.Date("Document Date", tracking=2)
    transporter_doc_no = fields.Char("Transporter Document No.", size=16, tracking=2)
    transportation_doc_date = fields.Date('Transport Document Date', tracking=2)
    consolidate_id = fields.Many2one('consolidate.bill', string="Consolidate Bill", tracking=2)
    sub_type_desc = fields.Text('Sub Type Description', tracking=2)
    bill_status = fields.Selection([('not', 'Not Generated'), ('generate', 'Generated'),
                                    ('cancel', 'Cancel')], string="Bill Status", default='not',
                                   tracking=2)
    logs_details = fields.Char("Log Details", copy=False, tracking=2)
    consolidate_eway = fields.Char("Consolidate Eway-Bill No", copy=False, tracking=2)
    cancel_date = fields.Char("E-Bill Cancel Date", copy=False, tracking=2)
    eway_bill_date = fields.Char("Eway-Bill date", copy=False, tracking=2)
    valid_ebill_date = fields.Char("Eway-ValidUp", copy=False, tracking=2)
    conslidate_ebill_date = fields.Char("Consolidate Ebill Date", copy=False, tracking=2)
    ewaybill_response = fields.Text('Eway Bill Response')
    ewaybill_print_response = fields.Text('Eway Bill Print Response')
    street = fields.Char('Street', tracking=2)
    street2 = fields.Char('Street2', tracking=2)
    zip = fields.Char('Pincode', change_default=True, tracking=2)
    city = fields.Char('City/Place', tracking=2)
    state_id = fields.Many2one("res.country.state", string='State', domain="[('country_id.code', '=', 'IN')]",
                               tracking=2)
    vat = fields.Char(string='GSTIN', help="GSTIN Number", tracking=2)
    transaction_type = fields.Selection([('1', 'Regular'),
                                         ('2', 'Bill To - Ship To'),
                                         ('3', 'Bill From - Dispatch From'),
                                         ('4', 'Combination of 2 and 3')], string="Transaction Type", copy=False,
                                        tracking=2, default='1')

    @api.constrains('doc_date')
    def validate_document_date(self):
        if self.doc_date:
            if self.doc_date and datetime.strptime(str(self.doc_date), "%Y-%m-%d").date() > datetime.now().date():
                raise UserError(_('Document Date Cannot be greater then today!'))
            return True

    @api.constrains('transportation_doc_date')
    def validate_transportation_doc_date(self):
        if self.doc_date and self.transportation_doc_date:
            if not (self.transportation_doc_date >= self.doc_date):
                raise UserError(_('Transport Document Date should be greater or equal to Document Date!'))
            return True

    @api.onchange('generate_ewaybill')
    def onchange_generate_ewaybill(self):
        address = self.picking_type_id.warehouse_id.partner_id
        if self.generate_ewaybill and address:
            self.street = address.street
            self.street2 = address.street2
            self.city = address.city
            self.state_id = address.state_id.id
            self.zip = address.zip
            self.vat = address.vat

    @api.onchange('transporter_id')
    def _onchange_transporter_id(self):
        if self.transporter_id:
            self.trans_id = self.transporter_id.vat

    def format_date(self, doc_date):
        if doc_date:
            return datetime.strptime(str(doc_date), DEFAULT_SERVER_DATE_FORMAT).strftime('%d/%m/%Y')
        else:
            return ''

    def get_configuration(self):
        configuration = self.env['eway.configuration'].search([], limit=1)
        if not configuration:
            raise UserError(_('Eway bill Configuration not found !'))
        return configuration

    def get_eway_bill_details(self):
        configuration = self.get_configuration()
        details_response = configuration.get_eway_details('GetEwayBill', self.ewaybill_no)
        print('details_response.json()....', details_response.json())
        return details_response.json()

    def print_eway_bill(self):
        Attachment = self.env['ir.attachment']
        configuration = self.get_configuration()
        details_response = self.get_eway_bill_details()
        det_response = details_response
        # Temporary to be able to use Print API
        # det_response['userGstin'] = '09AAFCT8324E1Z9'
        # det_response['fromGstin'] = '09AAFCT8324E1Z9'
        print_response = configuration.print_eway('printewb', det_response)
        attachment_data = {
            'name': 'Eway Bill: ' + str(self.origin or '') + ':' + str(self.name),
            'datas': base64.b64encode(print_response),
            'type': 'binary',
            'res_model': 'stock.picking',
            'res_id': self.id,
        }
        attachment = Attachment.create(attachment_data)
        print('attachment...', attachment)
        self.env.user.notify_success(message='EwayBill Printed Successfully! Please check '
                                             'the attachments at the bottom.')
        return True

    def print_eway_bill_details(self):
        Attachment = self.env['ir.attachment']
        configuration = self.get_configuration()
        details_response = self.get_eway_bill_details()
        det_response = details_response
        # Temporary to be able to use Print API
        # det_response['userGstin'] = '09AAFCT8324E1Z9'
        # det_response['fromGstin'] = '09AAFCT8324E1Z9'
        print_response = configuration.print_eway('printdetailewb', det_response)
        attachment_data = {
            'name': 'Detailed Eway Bill ' + str(self.origin or '') + ':' + str(self.name),
            'datas': base64.b64encode(print_response),
            'type': 'binary',
            'res_model': 'stock.picking',
            'res_id': self.id,
        }
        attachment = Attachment.create(attachment_data)
        print('attachment...', attachment)
        self.env.user.notify_success(message='Detailed EwayBill Printed Successfully! Please check '
                                             'the attachments at the bottom.')
        return True

    def generate_eway(self):
        tax_obj = self.env['account.tax']
        if self.ewaybill_no and self.bill_status == 'generate':
            raise UserError(_('You are not allow to Re-generate the Eway bill Again, Please cancel first !'))
        if not self.origin:
            raise UserError(_('Please fill Source Document!'))
        if not self.picking_type_id.warehouse_id:
            raise UserError(_('Warehouse is not set on Picking Operation %s !') % self.picking_type_id.name)
        if not self.picking_type_id.warehouse_id.partner_id:
            raise UserError(_('Address is not set on Warehouse %s !') % self.picking_type_id.warehouse_id.name)
        if not self.partner_id:
            raise UserError(_('Delivery Address is not set %s !') % self.name)
        if not self.partner_id.street:
            raise UserError(_('Street is not set on Delivery Address %s !') % self.partner_id.name)
        if not self.partner_id.street2:
            raise UserError(_('Street2 is not set on Delivery Address %s !') % self.partner_id.name)
        if not self.partner_id.city:
            raise UserError(_('City is not set on Delivery Address %s !') % self.partner_id.name)
        if not self.partner_id.state_id:
            raise UserError(_('State is not set on Delivery Address %s !') % self.partner_id.name)
        if not self.partner_id.zip:
            raise UserError(_('Pincode is not set on Delivery Address %s !') % self.partner_id.name)
        if not self.partner_id.vat:
            raise UserError(_('GSTIN is not set on Delivery Address %s !') % self.partner_id.name)
        port_other_country = self.env['res.country.state'].search([
            ('name', 'ilike', 'OTHER COUNTRIES')], limit=1)
        if not port_other_country:
            raise UserError(_('"OTHER COUNTRIES"  State not found !'))
        order_dic = {
            'supplyType': self.supply_type,
            'subSupplyType': self.sub_supply_type,
            'subSupplyDesc': self.sub_type_desc or '',
            'docType': self.document_type,
            'docNo': self.origin,
            'docDate': self.format_date(self.doc_date),
            'transactionType': int(self.transaction_type),
            'fromGstin': self.vat,
            # 'fromGstin': '05AAACG1539P1ZH',
            'fromTrdName': self.picking_type_id.warehouse_id.partner_id.name,
            'fromAddr1': self.street,
            'fromAddr2': self.street2,
            'fromPlace': self.city,
            'fromPincode': int(str(self.zip).replace(' ', '')) if self.zip else '',
            'actFromStateCode': self.state_id.port_code,
            'fromStateCode': self.state_id.port_code,
            # 'dispatchFromGSTIN': '02EHFPS5910D2Z0',
            # 'dispatchFromGSTIN': self.vat,
            # 'dispatchFromTradeName': self.picking_type_id.warehouse_id.partner_id.name,
            'toGstin': self.partner_id.vat,
            # 'toGstin': '02EHFPS5910D2Z0',
            'toTrdName': self.partner_id.name,
            'toAddr1': self.partner_id.street or '',
            'toAddr2': self.partner_id.street2 or '',
            'toPlace': self.partner_id.city or '',
            'toPincode': int(str(self.partner_id.zip).replace(' ', '')) if self.partner_id.zip else '',
            'actToStateCode': self.partner_id.state_id.port_code,
            'toStateCode': self.partner_id.state_id.port_code,
            # 'shipToGSTIN': '02EHFPS5910D2Z0',
            # 'shipToGSTIN': self.partner_id.vat or '',
            # 'shipToTradeName': self.partner_id.name,
            'transporterId': self.trans_id or '',
            'transporterName': self.transporter_id.name or '',
            'transDocNo': self.transporter_doc_no or '',
            'transMode': self.transportation_mode,
            'transDocDate': self.format_date(self.transportation_doc_date) or '',
            'vehicleNo': self.vehicle_no or '',
            'vehicleType': self.vehicle_type,
        }
        amount_untaxed = 0
        company_currency_id = self.company_id.currency_id
        line_data = []
        total_cgst = total_igst = total_sgst = total_cess = total_cess_non_advol = 0.0
        if self.move_ids_without_package:
            for line in self.move_ids_without_package:
                if not line.product_uom.uom_mapping_id:
                    raise UserError(_('Eway Code is not set on UOM "%s" ') % (line.product_uom.name))
                if not line.product_price > 0:
                    raise UserError(_('Unit Price is 0 for product "%s" ') % (line.product_id.name))
                if not line.product_id.l10n_in_hsn_code:
                    raise UserError(_('HSN CODE is blank for product "%s" ') % (line.product_id.name))
                if not line.quantity_done > 0:
                    raise UserError(_('Done Qty should be greater than 0 : product "%s" ') % (line.product_id.name))
                line_dic = {
                    'productName': line.product_id.name,
                    'productDesc': line.product_id.name,
                    'hsnCode': int(line.product_id.l10n_in_hsn_code)
                        if line.product_id.l10n_in_hsn_code else '',
                    'quantity': int(line.quantity_done),
                    'qtyUnit': line.product_uom.uom_mapping_id.code,
                }
                cgst_rate = sgst_rate = igst_rate = cess_rate = cess_non_advol = 0.0
                if self.document_type in ('INV', 'BIL', 'BOE'):
                    product_price = line.product_price
                    balance_taxes_res = line.tax_id._origin.compute_all(
                        product_price,
                        currency=company_currency_id,
                        quantity=line.product_uom_qty,
                        product=line.product_id,
                        partner=self.partner_id,
                        is_refund=False,
                        handle_price_include=True,
                    )
                    print('balance_taxes_res..', balance_taxes_res)
                    for tax_dict in balance_taxes_res.get('taxes', []):
                        print('tax_dict...', tax_dict)
                        tax = tax_obj.browse(tax_dict.get('id'))
                        if 'IGST' in tax_dict.get('name') or tax.name.startswith('IGST'):
                            igst_rate = tax.amount
                            total_igst += tax_dict.get('amount', 0.0)
                        elif 'CGST' in tax_dict.get('name') or tax.name.startswith('CGST'):
                            cgst_rate = tax.amount
                            total_cgst += tax_dict.get('amount', 0.0)
                        elif 'SGST' in tax_dict.get('name') or tax.name.startswith('SGST'):
                            sgst_rate = tax.amount
                            total_sgst += tax_dict.get('amount', 0.0)
                        elif 'CESS' in tax_dict.get('name') or tax.name.startswith('CESS'):
                            cess_rate = tax.amount
                            total_cess += tax_dict.get('amount', 0.0)
                    cess_non_advol = line.cess_non_advol
                    total_cess_non_advol += int(cess_non_advol) if cess_non_advol else 0
                line_dic.update({
                    'cgstRate': cgst_rate,
                    'sgstRate': sgst_rate,
                    'igstRate': igst_rate,
                    'cessRate': cess_rate,
                    'cessNonAdvol': int(cess_non_advol) if cess_non_advol else 0,
                    'taxableAmount': line.product_price * line.quantity_done,
                })
                amount_untaxed += line.product_price * line.quantity_done
                line_data.append(line_dic)
        order_dic.update({
            'itemList': line_data,
            'cgstValue': total_cgst,
            'sgstValue': total_sgst,
            'igstValue': total_igst,
            'totalValue': amount_untaxed,
            'otherValue': 0,
            'cessValue': total_cess,
            'cessNonAdvolValue': total_cess_non_advol,
            'totInvValue': amount_untaxed + total_cgst + total_sgst + total_igst + total_cess +
                           total_cess_non_advol,
        })
        print('order_dic...', order_dic)
        # tt
        configuration = self.get_configuration()
        # search = geo_query_address(street=self.company_id.partner_id.street, zip=self.partner_id.zip,
        #                            city=self.partner_id.city, state=self.company_id.partner_id.state_id.port_code,
        #                            country=self.company_id.partner_id.country_id.name)
        # Distance Calculation
        if self.transportation_distance > 0:
            order_dic.update({'transDistance': str(int(self.transportation_distance))})
        else:
            if configuration.distance_key and self.company_id.partner_id.zip and self.partner_id.zip:
                url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="\
                      + self.company_id.partner_id.zip + "&destinations=" + self.partner_id.zip + \
                      "&key=" + configuration.distance_key
                try:
                    response = requests.get(url, timeout=20.000).json()
                    print('response....', response)
                    if (response['status'] == 'OK'):
                        result = response.get('rows')
                        print('result...', result)
                        if result:
                            elements_list = response.get('rows')[0].get('elements')
                            if elements_list:
                                pre_final_list = elements_list[0]
                                if (pre_final_list.get('status') == 'OK'):
                                    final_list = (pre_final_list.get('distance')).get('value')
                                    if final_list > 1:
                                        distance_km = round(final_list * 0.001)
                                        print('distance_km...', distance_km)
                                        order_dic.update({'transDistance': str(int(distance_km))})
                                        self.transportation_distance = distance_km
                        else:
                            raise Warning(_('Invalid JSon for the Distance:\n%s') % result)
                    else:
                        raise Warning(_('Distance Error :%s could not be generated') % response)
                except Exception as e:
                    _logger.info("Exception in fetching Distance: %s", e.args)
            else:
                raise UserError(_('Invalid configuration for the Distance API'))
        # for Outward
        if self.supply_type == 'O':
            if self.document_type == 'BIL':
                if self.sub_supply_type == '9':
                    order_dic.update({
                        'actToStateCode': port_other_country.code,
                        'toStateCode': port_other_country.code
                    })
            # elif self.document_type == 'CHL':
            #     if self.sub_supply_type == '5':
            #         order_dic.update({
            #             'cgstValue': 0.0, 'sgstValue': 0.0, 'igstValue': 0.0
            #         })
            if self.sub_supply_type == '3':
                order_dic.update({
                    'actToStateCode': port_other_country.code,
                    'toStateCode': port_other_country.code
                })
        # # FOR iNWARD PROCESS
        # if self.supply_type == 'I' and self.document_type == 'INV':
        #     if self.sub_supply_type == '1':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': self.vat})
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': self.vat})
        # elif self.supply_type == 'I' and self.document_type == 'BIL':
        #     if self.sub_supply_type == '1':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': self.vat})
        #     elif self.sub_supply_type == '2' and port_other_country:
        #         order_dic.update({
        #             'toGstin': self.vat, 'fromStateCode': port_other_country.code,
        #             'actFromStateCode': port_other_country.code,
        #             'fromGstin': self.company_id.vat,
        #         })
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': self.vat})
        # elif self.supply_type == 'I' and self.document_type == 'BIL':
        #     if self.sub_supply_type == '2' and port_other_country:
        #         order_dic.update({
        #             'toGstin': self.vat, 'fromStateCode': port_other_country.code,
        #             'actFromStateCode': port_other_country.code, 'fromGstin': self.company_id.vat
        #         })
        # elif self.supply_type == 'I' and self.document_type == 'OTH':
        #     if self.sub_supply_type == '8':
        #         order_dic.update({
        #             'fromGstin': self.company_id.vat, 'toGstin': self.vat
        #         })
        # if self.supply_type == 'I' and self.document_type == 'CHL':
        #     if self.sub_supply_type == '12':
        #         order_dic.update({
        #             'fromGstin': self.company_id.vat,
        #             'toGstin': self.vat
        #         })
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': self.vat})
        #     elif self.sub_supply_type == '6' or self.sub_supply_type == '7' or self.sub_supply_type == '5':
        #         order_dic.update({
        #             'fromGstin': self.company_id.vat,
        #             'toGstin': self.vat
        #         })
        # if self.supply_type == 'I' and self.document_type == 'BOE':
        #     if self.sub_supply_type == '2' and port_other_country:
        #         order_dic.update({
        #             'fromGstin': self.company_id.vat,
        #             'actFromStateCode': port_other_country.code,
        #             'fromStateCode': port_other_country.code,
        #             'toGstin': self.vat
        #         })
        #     elif self.sub_supply_type == '9' and port_other_country:
        #         order_dic.update({
        #             'fromGstin': self.company_id.vat,
        #             'actFromStateCode': port_other_country.code,
        #             'fromStateCode': port_other_country.code,
        #             'toGstin': self.vat
        #         })

        # if self.supply_type == 'O' and self.document_type == 'INV':
        #     if self.sub_supply_type == '1' or self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': configuration.gstin,
        #                           'docType': self.document_type})
        #
        #     elif self.sub_supply_type == '3' and port_other_country:
        #         order_dic.update({'fromGstin': configuration.gstin, 'actToStateCode': port_other_country.code,
        #                           'toStateCode': port_other_country.code})
        #
        # elif self.supply_type == 'O' and self.document_type == 'BIL':
        #     if self.sub_supply_type == '1':
        #         order_dic.update({'fromGstin': configuration.gstin,
        #                           'docType': self.document_type})
        #     elif self.sub_supply_type == '3':
        #         order_dic.update({'fromGstin': configuration.gstin, 'actToStateCode': port_other_country.code,
        #                           'toStateCode': port_other_country.code,
        #                           'docType': self.document_type})
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': configuration.gstin, 'actToStateCode': port_other_country.code,
        #                           'toStateCode': port_other_country.code,
        #                           'docType': self.document_type})
        #
        # elif self.supply_type == 'O' and self.document_type == 'CHL':
        #     if self.sub_supply_type == '9' or self.sub_supply_type == '10' or self.sub_supply_type == '4' or self.sub_supply_type == '11':
        #         order_dic.update({ # 'fromGstin': configuration.gstin,
        #                           'docType': self.document_type})
        #     elif self.sub_supply_type == '5':
        #         order_dic.update({'fromGstin': configuration.gstin,
        #                           'cgstValue': 0.0, 'sgstValue': 0.0, 'igstValue': 0.0, })
        #     elif self.sub_supply_type == '3' and port_other_country:
        #         order_dic.update(
        #             {'fromGstin': configuration.gstin, 'actToStateCode': port_other_country.code,
        #              'toStateCode': port_other_country.code})
        #
        # elif self.supply_type == 'O' and self.document_type == 'OTH':
        #     if self.sub_supply_type == '11':
        #         order_dic.update({'fromGstin': configuration.gstin,
        #                           'docType': self.document_type})
        #     elif self.sub_supply_type == '9':
        #
        #         order_dic.update({'fromGstin': configuration.gstin,
        #                           'docType': self.document_type,
        #                           'subSupplyDesc': self.sub_type_desc, })
        #
        # # FOR INWARD PROCESS
        # if self.supply_type == 'I' and self.document_type == 'INV':
        #     if self.sub_supply_type == '1':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin})
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin})
        # elif self.supply_type == 'I' and self.document_type == 'BIL':
        #     if self.sub_supply_type == '1':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin})
        #     elif self.sub_supply_type == '2' and port_other_country:
        #         order_dic.update({'toGstin': configuration.gstin, 'fromStateCode': port_other_country.code,
        #                           'actFromStateCode': port_other_country.code,
        #                           'fromGstin': self.company_id.vat,
        #                           'docType': self.document_type})
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin})
        # elif self.supply_type == 'I' and self.document_type == 'BIL':
        #     if self.sub_supply_type == '2' and port_other_country:
        #         order_dic.update({'toGstin': configuration.gstin, 'fromStateCode': port_other_country.code,
        #                           'actFromStateCode': port_other_country.code, 'fromGstin': self.company_id.vat,
        #                           'docType': self.document_type})
        # elif self.supply_type == 'I' and self.document_type == 'OTH':
        #     if self.sub_supply_type == '8':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin,
        #                           'docType': self.document_type,
        #                           'subSupplyDesc': self.sub_type_desc,
        #                           })
        # if self.supply_type == 'I' and self.document_type == 'CHL':
        #     if self.sub_supply_type == '12':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin,
        #                           'docType': self.document_type,
        #                           })
        #     elif self.sub_supply_type == '9':
        #         order_dic.update({'fromGstin': self.company_id.vat, 'toGstin': configuration.gstin})
        #
        #     elif self.sub_supply_type == '6' or self.sub_supply_type == '7' or self.sub_supply_type == '5':
        #         order_dic.update({'fromGstin': self.company_id.vat,
        #                           'toGstin': configuration.gstin,
        #                           'docType': self.document_type
        #                           })
        # if self.supply_type == 'I' and self.document_type == 'BOE':
        #     if self.sub_supply_type == '2' and port_other_country:
        #         order_dic.update({'fromGstin': self.company_id.vat,
        #                           'actFromStateCode': port_other_country.code,
        #                           'fromStateCode': port_other_country.code, 'toGstin': configuration.gstin,
        #                           'docType': self.document_type
        #                           })
        #     elif self.sub_supply_type == '9' and port_other_country:
        #         order_dic.update({'fromGstin': self.company_id.vat,
        #                           'actFromStateCode': port_other_country.code,
        #                           'fromStateCode': port_other_country.code, 'toGstin': configuration.gstin,
        #                           'docType': self.document_type
        #                           })
        # print('order_dic final..+++++++++++++++++++++++++..', order_dic)
        # order_dic = {
        #     'supplyType': 'O', 'subSupplyType': '1', 'subSupplyDesc': '', 'docType': 'INV', 'docNo': 'WH/OUT/00022 ',
        #     'docDate': '24/09/2020', 'fromGstin': '09AAFCT8324E1Z9', 'fromTrdName': 'Technogeo soft Pvt LTD',
        #     'fromAddr1': 'H49', 'fromAddr2': 'Sector 63', 'fromPlace': 'Noida', 'fromPincode': 201301,
        #     'actFromStateCode': '09', 'fromStateCode': '09', 'toGstin': '27AAFCG3720R1Z7',
        #     'toTrdName': 'GOQII TECHNOLOGIES PRIVATE LIMITED',
        #     'toAddr1': '101, SATYAM TOWERS, SANGHAVI CORPORATE PARK', 'toAddr2': 'OFF BKSD MARG, DEONAR, GOVANDI EAST',
        #     'toPlace': 'Mumbai City', 'toPincode': 400088, 'actToStateCode': 27, 'toStateCode': 27,
        #     'transactionType': '1', 'transporterId': '', 'transporterName': '', 'transDocNo': '', 'transMode': '1',
        #     'transDocDate': '', 'vehicleNo': 'UP13AV9990', 'vehicleType': 'R', 'cgstValue': 0, 'sgstValue': 0,
        #     'igstValue': 300.67, 'itemList': [
        #         {'productName': 'BLAZER-1', 'productDesc': 'BLAZER-1', 'hsnCode': 4421, 'quantity': 25,
        #          'qtyUnit': 'NOS', 'cgstRate': 0, 'sgstRate': 0, 'igstRate': 3, 'cessRate': 3, 'cessNonadvol': 0,
        #          'taxableAmount': 5609889},
        #         {'productName': 'BLAZER-2', 'productDesc': 'BLAZER-2', 'hsnCode': 4421, 'quantity': 25,
        #          'qtyUnit': 'NOS', 'cgstRate': 0, 'sgstRate': 0, 'igstRate': 3, 'cessRate': 3, 'cessNonadvol': 0,
        #          'taxableAmount': 5609889}], 'totalValue': 56099, 'totInvValue': 68358, 'otherValue': '-100',
        #     'cessValue': 400.56, 'cessNonAdvolValue': 400
        # }
        # print('order_dic.22..', order_dic)
        data_base64 = json.dumps(order_dic)
        print('data_base64...', data_base64)
        response = configuration.generate_eway(data_base64, 'GENEWAYBILL')
        response_json = response.json()
        print('Generate response...', response_json)
        if response_json.get('status_code', '') == 200 or 'ewayBillNo' in response_json:
            self.ewaybill_no = response_json.get('ewayBillNo')
            self.eway_bill_date = response_json.get('ewayBillDate')
            self.valid_ebill_date = response_json.get('validUpto')
            self.bill_status = 'generate'
            self.logs_details = ""
            self.cancel_date = ''
            self.message_post(body=_("Eway Bill is generated : '" + str(self.ewaybill_no) +
                "', Eway Bill Date: '" + str(self.eway_bill_date) + "', Valid Upto: '"
                + str(self.valid_ebill_date)))
            if response_json.get('alert'):
                self.message_post(body=_("Eway Bill Alert : '" + str(response_json.get('alert'))))
            self.env.user.notify_success(message='EwayBill Generated Successfully!')
            # Print and attach
            self.print_eway_bill()
        else:
            self.logs_details = response_json.get('error', {}).get('message', '')
            self.env.user.notify_danger(message=response_json.get('error', {}).get('message'))
        return True
