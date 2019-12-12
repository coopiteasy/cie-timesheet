# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import time
from openerp import models, api, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    analytic_account_ids = fields.Many2many(
        comodel_name="account.analytic.account", string="Analytic Accounts"
    )
