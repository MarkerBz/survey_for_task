# -*- coding: utf-8 -*-

from odoo import models


class ProcurementOrder(models.Model):
    _inherit = "procurement.order"
    
    def _create_service_task(self):
        res = super(ProcurementOrder, self)._create_service_task()
        
        # Get survey and its template from product
        survey = self.product_id.survey_id
        survey_email_template = self.product_id.survey_email_template_id
        
        if (not survey) or (not survey_email_template):
            return res
        
        # Adjust survey parameters
        survey.users_can_go_back = True
        survey.auth_required = True
        
        # Link survey to task
        self.task_id.survey_id = survey
        
        # Create survey compose wizard and send email:
        
        partner_id = self.sale_line_id.order_id.partner_id.id or self.partner_dest_id.id
        subject = u'Техническое Задание для задачи (%s)' % self.task_id.name
        template = survey_email_template
        
        survey_email_wizard = self.env['survey.mail.compose.message'] \
            .sudo() \
            .with_context(
                self.env.context,
                active_model = 'survey.survey',
                active_ids = [survey.id],
                active_id = survey.id,
                default_model = 'survey.survey',
                default_res_id = survey.id,
                default_use_template = bool(template),
                default_template_id = template and template.id or False,
                default_composition_mode = 'comment') \
            .create({
                'survey_id':    survey.id,
                'public':       'email_private',
                'partner_ids':  [(4, partner_id)],
                'subject':      subject})
        survey_email_wizard.onchange_template_id_wrapper()
        survey_email_wizard.send_mail()
        
        return res
