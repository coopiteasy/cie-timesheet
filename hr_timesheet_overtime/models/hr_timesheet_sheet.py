# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp import api, fields, models, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    daily_working_hours = fields.Float('Daily Working Hours',
                                       readonly=True,
                                       compute='_compute_daily_working_hours',
                                       help="Hours to work for today")

    total_overtime = fields.Float('Total Overtime Hours',
                                  readonly=True,
                                  compute='_compute_total_overtime',
                                  help='Total of overtime hours')

    @api.depends('employee_id')
    def _compute_daily_working_hours(self):
        self.daily_working_hours = self._get_working_hours()

    @api.depends('employee_id', 'period_ids', 'timesheet_ids')
    def _compute_total_overtime(self):
        current_overtime = self._get_initial_overtime()
        total_timesheet_day = self._get_worked_hours_per_day()
        for date in total_timesheet_day:
            daily_wh = self._get_working_hours(date=datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT))
            daily_overtime = total_timesheet_day[date] - daily_wh
            current_overtime += daily_overtime

        self._write_hr_employee(current_overtime)
        self.total_overtime = current_overtime

    def _get_working_hours(self, date=None):
        total = 0.0
        contracts = self.env['hr.contract'] \
            .sudo() \
            .search([
                ("employee_id.id", "=", self.employee_id.id)
            ])
        # ValueError: Expected singleton: hr_timesheet_sheet.sheet(2, 1)
        for contract in contracts:
            for calendar in contract.working_hours:
                for wh in calendar.get_working_hours_of_date(start_dt=date):
                    total += wh

        return total

    # TODO define a starting date
    def _get_total_timesheet_day(self):
        ts_day = self.env['hr_timesheet_sheet.sheet.day'] \
            .search([
                ("sheet_id.employee_id.id", "=", self.employee_id.id)
            ])
        return {ts.name: ts.total_timesheet for ts in ts_day}

    # TODO define a starting date
    def _get_worked_hours_per_day(self):
        aal = self.env['account.analytic.line'] \
            .search([
                ("user_id.id", "=", self.employee_id.user_id.id)
            ])

        total_day = {}
        for line in aal:
            if line.date in total_day:
                total_day[line.date] += line.unit_amount
            else:
                total_day[line.date] = line.unit_amount
        return total_day

    # TODO define a starting date
    def _get_initial_overtime(self):
        overtime = 0.0
        employee = self.env['hr.employee'] \
            .search([
                ("user_id.id", "=", self.employee_id.user_id.id)
            ])
        if employee:
            overtime = employee.initial_overtime
        return overtime

    def _write_hr_employee(self, overtime):
        self.env['hr.employee'] \
            .sudo() \
            .search([
                ("user_id.id", "=", self.employee_id.user_id.id)
            ]) \
            .write({
                "total_overtime": overtime
            })
