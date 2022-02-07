# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from datetime import date, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    active = fields.Boolean("Active", default=True)
    # Numeric fields
    daily_working_hours = fields.Float(
        "Daily Working Hours",
        related="employee_id.current_day_working_hours",
        help="Hours to work for the current day",
    )
    daily_overtime = fields.Float(
        "Daily Overtime",
        compute="_compute_daily_overtime",
        help="Overtime for the current day",
    )
    timesheet_overtime = fields.Float(
        "Timesheet Overtime",
        compute="_compute_timesheet_overtime",
        help="Overtime for this timesheet period",
    )
    total_overtime = fields.Float(
        "Overtime Total",
        related="employee_id.total_overtime",
        help="Overtime total since employee's overtime start date",
        store=True,
    )

    def get_worked_hours(self, start_date, end_date=None):
        """
        Get total of worked hours from account analytic lines
        for a given date range
        @param start_date: date
        @param end_date: date
        @return: total of worked hours
        """
        self.ensure_one()
        if end_date is None:
            end_date = start_date
        aal = self.env["account.analytic.line"].search(
            [
                ("sheet_id", "=", self.id),
                ("date", ">=", start_date),
                ("date", "<=", end_date),
            ]
        )
        return sum(line.unit_amount for line in aal)

    @api.multi
    def _compute_daily_overtime(self):
        """
        Computes overtime for the current day
        """
        current_day = date.today()
        for sheet in self:
            working_hours = sheet.employee_id.get_working_hours(current_day)
            worked_hours = sheet.get_worked_hours(current_day)
            sheet.daily_overtime = worked_hours - working_hours

    @api.multi
    def _compute_timesheet_overtime(self):
        """
        Computes overtime for the timesheet period
        (from the start date (included) to the current date (not included))
        """
        current_day = date.today()
        for sheet in self:
            employee = sheet.employee_id
            start_date = sheet.date_start
            end_date = sheet.date_end
            if (
                current_day < start_date
                or employee.overtime_start_date > end_date
            ):
                sheet.timesheet_overtime = 0.0
                continue
            if employee.overtime_start_date > start_date:
                start_date = employee.overtime_start_date
            if current_day <= end_date:
                end_date = current_day - timedelta(days=1)

            working_hours = employee.get_working_hours(start_date, end_date)
            worked_hours = sheet.get_worked_hours(start_date, end_date)
            sheet.timesheet_overtime = worked_hours - working_hours
