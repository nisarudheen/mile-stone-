from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    milestone = fields.Integer(string='Milestone')
    task_id = fields.Many2one('project.task', string='Task')
