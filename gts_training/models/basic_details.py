from odoo import models, fields, api, _


class BasicDetails(models.Model):
    _name = 'geo.tech'

    title = fields.Selection([('mr', 'MR.'),
                               ('mrs', 'Mrs')
                               ], 'Title')
    name = fields.Char('Name')
    age = fields.Integer('Age')
    address = fields.Char('Address')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')
                               ], 'Gender')
    amount = fields.Float('Amount')
    working = fields.Boolean('Working')
    salary_id = fields.Many2one('salary.salary', string='Salary')
    salary_ids = fields.Many2many('salary.salary', string="Salary's")
    add = fields.Integer('Add')
    sub = fields.Integer('Sub')
    total = fields.Integer('total', compute='_compute_total_amount')


    @api.onchange('title')
    def onchange_gender(self):
        if self.title == 'mr':
            self.gender = 'male'

        elif self.title == 'mrs':
            self.gender = 'female'

    @api.depends('add', 'sub')
    def _compute_total_amount(self):
        for data in self:
            self.total = data.add + data.sub

    def salary_create(self):
        # for data in self:
        #     salary_obj = self.env['salary.salary'].create({
        #         'name': data.name,
        #         'description': data.address,
        #     })
        #
        # print(salary_obj, '===========')

        sal_obj = self.env['salary.salary'].search([('name', '=', self.name)], limit=1)
        # for salary in sal_obj:
        #     print(salary.name, 'nameeeee')
        print(sal_obj, 'pppppppp')
        print(sal_obj.id, 'IDDDDDDDD')
