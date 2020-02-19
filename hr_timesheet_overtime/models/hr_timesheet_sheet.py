# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models
from datetime import timedelta


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    daily_working_hours = fields.Float(
        "Daily Working Hours",
        readonly=True,
        compute="_compute_daily_working_hours",
        help="Hours to work for the current day",
    )

    daily_overtime = fields.Float(
        "Daily Overtime",
        readonly=True,
        compute="_compute_daily_overtime",
        help="Overtime for the current day",
    )

    timesheet_overtime = fields.Float(
        "Timesheet Overtime",
        readonly=True,
        compute="_compute_timesheet_overtime",
        help="Overtime for this timesheet period",
    )

    total_overtime = fields.Float(
        "Overtime Total",
        readonly=True,
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
            sheet.daily_working_hours = sheet.get_working_hours(
                date=current_day
            )

    @api.multi
    def _compute_daily_overtime(self):
        """
        Computes overtime for the current day
        """
        current_day = fields.Date.today()
        for sheet in self:
            working_hours = sheet.get_working_hours(date=current_day)
            worked_hours = sheet.get_worked_hours(current_day)
            sheet.daily_overtime = worked_hours - working_hours

    @api.multi
    def _compute_timesheet_overtime(self):
        """
        Computes overtime for the timesheet period
        (from the start date to the current date not included)
        """
        current_day = fields.Date.today()
        for sheet in self:
            ts_overtime = 0.0
            total_timesheet_period = sheet.get_total_timesheet_period()
            for date, total_timesheet in total_timesheet_period.items():
                if current_day > date >= sheet.employee_id.overtime_start_date:
                    daily_wh = sheet.get_working_hours(date=date)
                    daily_overtime = total_timesheet - daily_wh
                    ts_overtime += daily_overtime

            sheet.timesheet_overtime = ts_overtime

    @api.multi
    def get_working_hours(self, date=None):
        """
        Get the working hours for a given date according to employee's contracts
        @param date: string object
        @return: total of working hours
        """
        self.ensure_one()
        start_dt = None
        if date:
            start_dt = fields.Datetime.from_string(date)
        total = 0.0
        contracts = self.get_contracts(self.employee_id)
        for contract in contracts:
            for calendar in contract.working_hours:
                total += sum(
                    wh
                    for wh in calendar.get_working_hours_of_date(
                        start_dt=start_dt
                    )
                )
        return total

    def get_contracts(self, employee_id):
        return (
            self.env["hr.contract"]
            .sudo()
            .search([("employee_id.id", "=", employee_id.id)])
        )

    @api.multi
    def get_total_timesheet_period(self):
        """
        Get total_timesheet from hr_timesheet_sheet.sheet.day
        for each day of the timesheet period
        @return: dictionary {'date':'total_timesheet'}
        """
        self.ensure_one()
        ts_day = self.env["hr_timesheet_sheet.sheet.day"].search(
            [
                ("sheet_id.employee_id.id", "=", self.employee_id.id),
                ("sheet_id.date_from", ">=", self.date_from),
                ("sheet_id.date_to", "<=", self.date_to),
            ]
        )
        date_to = fields.Date.from_string(self.date_to)
        date_from = fields.Date.from_string(self.date_from)

        nb_days = (date_to - date_from).days + 1
        periods = {
            fields.Date.to_string(date_from + timedelta(days=d)): 0.0
            for d in range(0, nb_days)
        }
        periods.update({ts.name: ts.total_timesheet for ts in ts_day})
        return periods

    def get_worked_hours(self, date):
        """
        Get total of worked hours from account analytic lines
        for a given date
        @param date: string object
        @return: total of worked hours
        """
        self.ensure_one()
        worked_hours = 0.0
        aal = self.env["account.analytic.line"].search(
            [
                ("user_id.id", "=", self.employee_id.user_id.id),
                ("date", "=", date),
            ]
        )
        worked_hours += sum(line.unit_amount for line in aal)
        return worked_hours
