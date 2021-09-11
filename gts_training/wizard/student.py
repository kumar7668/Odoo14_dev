from odoo import models, fields, api, _


class Student(models.TransientModel):
    _name = 'student.student'
    _description = 'student'
    _rec_name = 'name'


    name = fields.Char('Name')
    text = fields.Char('Text')


    def create_student_record(self):
        pass

