# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from odoo import api, fields, models


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
        compute="_compute_total_overtime",
        help="Total Overtime since Overtime Start Date",
    )
    timesheet_sheet_ids = fields.One2many(
        comodel_name="hr_timesheet.sheet",
        inverse_name="employee_id",
        string="Timesheet sheets",
    )

    # Date fields
    overtime_start_date = fields.Date(
        string="Overtime Start Date",
        required=True,
        default=date.today().replace(month=1, day=1),
        help="Overtime Start Date to compute overtime",
    )

    has_overtime_access = fields.Boolean(
        string="Has access to overtime page",
        compute="_compute_has_overtime_access",
    )

    @api.multi
    def _compute_has_overtime_access(self):
        for rec in self:
            has_access = False
            if self.env.user.has_group(
                "hr.group_hr_manager"
            ) or self.env.user.has_group("hr.group_hr_user"):
                has_access = True
            elif (
                rec.user_id.employee_ids.parent_id.id
                == self.env.user.employee_ids.id
            ):
                has_access = True
            elif rec.user_id == self.env.user:
                has_access = True
            rec.has_overtime_access = has_access

    @api.multi
    @api.depends("timesheet_sheet_ids.active")
    def _compute_total_overtime(self):
        """
        Computes total overtime since employee's overtime start date
        """
        for employee in self:
            sheets = self.env["hr_timesheet.sheet"].search(
                [
                    ("employee_id", "=", employee.id),
                    ("date_end", ">=", employee.overtime_start_date),
                ]
            )
            overtime = sum(sheet.timesheet_overtime for sheet in sheets)
            employee.total_overtime = employee.initial_overtime + overtime
