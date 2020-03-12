# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import time

from openerp import models, api, fields


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    # Numeric fields
    initial_overtime = fields.Float(
        string="Initial Overtime",
        default=0.0,
        help="Initial Overtime to start Overtime Start Date with",
    )
    total_overtime = fields.Float(
        string="Total Overtime",
        default=0.0,
        readonly=True,
        compute="_compute_total_overtime",
        help="Total Overtime since Overtime Start Date",
    )

    # Date fields
    overtime_start_date = fields.Date(
        string="Overtime Start Date",
        required=True,
        default=time.strftime("%Y-01-01"),
        help="Overtime Start Date to compute overtime",
    )

    @api.multi
    def _compute_total_overtime(self):
        """
        Computes total overtime since employee's overtime start date
        """
        for employee in self:
            sheets = (
                self.env["hr_timesheet_sheet.sheet"]
                .search([("employee_id", "=", employee.id),])
                .filtered(
                    lambda s: s.date_from >= employee.overtime_start_date
                    or employee.overtime_start_date <= s.date_to
                )
            )
            overtime = sum(sheet.timesheet_overtime for sheet in sheets)
            employee.total_overtime = employee.initial_overtime + overtime
