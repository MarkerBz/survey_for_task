# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProjectTask(models.Model):
    _inherit = "project.task"
    
    survey_id = fields.Many2one('survey.survey', 'Survey')
    tot_completed_surveys = fields.Integer('Number of completed surveys',
                            compute='_compute_survey_statistic')
    
    @api.depends('survey_id.user_input_ids', 'survey_id', 'partner_id')
    def _compute_survey_statistic(self):
        for task in self:
            completed_surveys = self.env['survey.user_input'].search([
                ('survey_id', '=', task.survey_id.id),
                ('partner_id', '=', task.partner_id.id),
                ('state', '=', 'done'),
            ])
            task.tot_completed_surveys = len(completed_surveys)
    
    @api.multi
    def act_task_completed_surveys(self):
        self.ensure_one()
        user_inputs = self.env['survey.user_input'].search([
            ('survey_id', '=', self.survey_id.id),
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
