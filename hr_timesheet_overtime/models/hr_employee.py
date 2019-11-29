# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    initial_overtime = fields.Float(string='Initial Overtime', default=0.0)

    total_overtime = fields.Float(string='Total Overtime', default=0.0)

