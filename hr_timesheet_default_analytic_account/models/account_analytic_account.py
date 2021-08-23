# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    project_ids = fields.Many2many(
        comodel_name="project.project", string="Projects"
    )
