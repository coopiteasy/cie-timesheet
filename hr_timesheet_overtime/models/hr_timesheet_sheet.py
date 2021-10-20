# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import logging
from datetime import datetime, timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    active = fields.Boolean("Active", default=True)
    # Numeric fields
    daily_working_hours = fields.Float(
        "Daily Working Hours",
        compute="_compute_daily_working_hours",
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
    )

    @api.multi
    def _compute_daily_working_hours(self):
        """
        Computes working hours for the current day according to employee's contracts
        """
        current_day = fields.Date.today()
        for sheet in self:
            sheet.daily_working_hours = sheet.get_working_hours(current_day)

    @api.multi
    def _compute_daily_overtime(self):
        """
        Computes overtime for the current day
        """
        current_day = fields.Date.today()
        for sheet in self:
            working_hours = sheet.get_working_hours(current_day)
            worked_hours = sheet.get_worked_hours(current_day)
            sheet.daily_overtime = worked_hours - working_hours

    @api.multi
    def _compute_timesheet_overtime(self):
        """
        Computes overtime for the timesheet period
        (from the start date (included) to the current date (not included))
        """
        current_day = fields.Date.today()
        for sheet in self:
            ts_overtime = 0.0
            total_timesheet_per_day = sheet.get_total_timesheet_per_day()
            for date, total_timesheet_day in total_timesheet_per_day.items():
                if sheet.employee_id.overtime_start_date <= date < current_day:
                    daily_wh = sheet.get_working_hours(date)
                    daily_overtime = total_timesheet_day - daily_wh
                    ts_overtime += daily_overtime

            sheet.timesheet_overtime = ts_overtime

    @api.multi
    def get_working_hours(self, date):
        """
        Get the working hours for a given date according to employee's contracts
        @param date: string object
        @return: total of working hours
        """
        self.ensure_one()
        date_dt = datetime(date.year, date.month, date.day)
        total = 0.0
        contracts = self.get_contracts(date)
        for contract in contracts:
            for calendar in contract.resource_calendar_id:
                total += self.get_day_work_hours(date_dt, calendar)

        return total

    def get_day_work_hours(self, date_dt, calendar):
        work_time_per_day = self.employee_id.list_work_time_per_day(
            date_dt, date_dt + timedelta(days=1), calendar
        )
        if not work_time_per_day:
            return 0.0
        # .list_work_time_per_day() returns a list of tuples:
        # (date, work time)
        return work_time_per_day[0][1]

    def get_contracts(self, date):
        """
        Get employee's contracts whose given date is included
        in the start date and the end date (defined or not) of the contract
        @param date: string object
        @return: hr.contract object
        """
        return (
            self.env["hr.contract"]
            .sudo()
            .search(
                [
                    ("employee_id", "=", self.employee_id.id),
                    ("date_start", "<=", date),
                    "|",
                    ("date_end", "=", None),
                    ("date_end", ">=", date),
                ]
            )
        )

    @api.multi
    def get_total_timesheet_per_day(self):
        """
        Get the total hours for each day of the timesheet period
        @return: dictionary {'date':'total_timesheet'}
        """
        self.ensure_one()
        date_start = self.date_start
        nb_days = (self.date_end - date_start).days + 1
        totals_per_day = {
            date_start + timedelta(days=d): 0.0 for d in range(nb_days)
        }
        for timesheet in self.timesheet_ids:
            totals_per_day[timesheet.date] += timesheet.unit_amount
        return totals_per_day

    def get_worked_hours(self, date):
        """
        Get total of worked hours from account analytic lines
        for a given date
        @param date: string object
        @return: total of worked hours
        """
        self.ensure_one()
        aal = self.env["account.analytic.line"].search(
            [
                ("user_id.id", "=", self.employee_id.user_id.id),
                ("date", "=", date),
            ]
        )
        return sum(line.unit_amount for line in aal)
