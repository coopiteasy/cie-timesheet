# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from openerp import api, fields, models, _


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    def get_number_days_between_dates(self, date_from, date_to):
        """
        Returns number of days between two dates
        @param date_from: string object
        @param date_to: string object
        @return: integer
        """
        datetime_from = datetime.strptime(date_from, "%Y-%m-%d")
        datetime_to = datetime.strptime(date_to, "%Y-%m-%d")
        difference = datetime_to - datetime_from
        # return result and add a day
        return difference.days + 1

    def _prepare_analytic_line(self, date, account, sheet_id, user_id):
        return {
            "account_id": account.id,
            "amount": 0.0,
            "date": date,
            "is_timesheet": "True",
            "name": "/",
            "sheet_id": sheet_id,
            "unit_amount": 0,
            "user_id": user_id.id,
        }

    @api.model
    def create(self, vals):
        res = super(HrTimesheetSheet, self).create(vals)

        date_from = res["date_from"]
        date_to = res["date_to"]
        employee_id = res["employee_id"]
        sheet_id = res["id"]

        days = self.get_number_days_between_dates(date_from, date_to)
        for day in range(days):
            datetime_current = (
                datetime.strptime(date_from, "%Y-%m-%d") + timedelta(days=day)
            ).strftime("%Y-%m-%d")
            for account in employee_id.analytic_account_ids:
                aal_dict = self._prepare_analytic_line(
                    datetime_current, account, sheet_id, employee_id.user_id
                )
                res.write({"timesheet_ids": [(0, 0, aal_dict)]})
        return res
