# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import time
from openerp import models, api, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    initial_overtime = fields.Float(
        string="Initial Overtime",
        default=0.0,
        help="Initial Overtime to start Overtime Start Date with",
    )

    total_overtime = fields.Float(
        string="Total Overtime",
        default=0.0,
        help="Total Overtime since Overtime Start Date",
    )

    overtime_start_date = fields.Date(
        string="Overtime Start Date",
        required=True,
        default=time.strftime("%Y-01-01"),
        help="Overtime Start Date to compute overtime",
    )
