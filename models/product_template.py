# -*- coding: utf-8 -*-

from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    survey_id = fields.Many2one('survey.survey', 'Survey')
    survey_email_template_id = fields.Many2one('mail.template', 'Email Template')
