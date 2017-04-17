# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    tot_completed_surveys = fields.Integer('Number of completed surveys',
                            compute='_compute_survey_statistic')
    
    @api.depends('tasks_ids.survey_id.user_input_ids', 'tasks_ids.survey_id', 'partner_id')
    def _compute_survey_statistic(self):
        for order in self:
            completed_surveys = self.env['survey.user_input'].search([
                ('survey_id', 'in', [t.survey_id.id for t in order.tasks_ids]),
                ('partner_id', '=', order.partner_id.id),
                ('state', '=', 'done'),
            ])
            order.tot_completed_surveys = len(completed_surveys)
    
    @api.multi
    def act_task_completed_surveys(self):
        self.ensure_one()
        survey_ids = [t.survey_id.id for t in self.tasks_ids]
        user_inputs = self.env['survey.user_input'].search([
            ('survey_id', 'in', survey_ids),
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'done'),
        ])
        if not user_inputs:
            return
        elif len(user_inputs) == 1:
            view_mode = 'form,tree'
            res_id = user_inputs.id
        else:
            view_mode = 'tree,form'
            res_id = False
        return {
            'name':         u'Ответы',
            'type':         'ir.actions.act_window',
            'res_model':    'survey.user_input',
            'view_type':    'form',
            'view_mode':    view_mode,
            'res_id':       res_id,
            'domain': [('id', 'in', user_inputs.ids)],
        }
