from odoo import models, fields, api


class SaleOrderButton(models.Model):
    _inherit = 'sale.order'

    is_update = fields.Boolean(string='Update')
    project_id = fields.Many2one('project.project', string='Project')

    def create_milestone(self):
        project = self.env['project.project'].create({
            'name': self.name,
            'partner_id': self.partner_id.id
        })
        self.project_id = project.id
        values = []
        for rec in self.order_line:
            if rec.milestone not in values:
                values.append(rec.milestone)
                parent_task = self.env['project.task'].create({
                    'name': 'milestone' + str(rec.milestone),
                    'partner_id': self.partner_id.id,
                    'project_id': project.id,
                })

            sub_task = rec.env['project.task'].create(
                    {'name': 'milestone' + str(rec.milestone) +
                         rec.product_template_id.name,
                         'partner_id': self.partner_id.id,
                         'project_id': project.id,
                         'parent_id': parent_task.id
                         })
            rec.task_id = sub_task.id
            self.is_update = True

    def update_milestone(self):
        for rec in self.order_line:
            if not rec.task_id:
                task = self.project_id.mapped('task_ids').filtered(
                        lambda l: l.name == 'milestone' + str(rec.milestone))
                if task:
                    rec.env['project.task'].create(
                            {'name': 'milestone' + str(rec.milestone) +
                                     rec.product_template_id.name,
                             'partner_id': self.partner_id.id,
                             'project_id': self.project_id.id,
                             'parent_id': task.id
                             })
                else:
                    parent_task = rec.env['project.task'].create({
                        'name': 'milestone' + str(rec.milestone),
                        'project_id': self.project_id.id,
                    })
                    rec.env['project.task'].create(
                        {'name': 'milestone' + str(rec.milestone) +
                                 rec.product_template_id.name,
                         'partner_id': self.partner_id.id,
                         'project_id': self.project_id.id,
                         'parent_id': parent_task.id
                         })
