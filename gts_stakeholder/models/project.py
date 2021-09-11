from odoo import api, fields, models, _


class Project(models.Model):
    _inherit = 'project.project'

    stakeholder_ids = fields.One2many('stakeholder.lines', 'project_task_id', 'Stakeholder Lines')


class StakeholderLines(models.Model):
    _name = 'stakeholder.lines'

    project_task_id = fields.Many2one('project.project', 'Project Task')
    partner_id = fields.Many2one('res.partner', 'Name')
    role_id = fields.Many2one('project.role', 'Role')
    department_id = fields.Many2one('hr.department', 'Department')
    role_in_project = fields.Many2one('project.role', 'Role in Project')
    type_of_stakeholder = fields.Many2one('project.stakeholder', 'Type of Stakeholder')
    type_of_communication = fields.Many2one('project.communication', 'Type of Communication')
    expectations = fields.Text('Expectations')
