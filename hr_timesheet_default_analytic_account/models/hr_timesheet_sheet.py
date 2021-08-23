# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime, timedelta

from odoo import api, models


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    def get_number_days_between_dates(self, date_start, date_end):
        """
        Returns number of days between two dates
        @param date_start: string object
        @param date_end: string object
        @return: integer
        """
        datetime_from = datetime.strptime(date_start, "%Y-%m-%d")
        datetime_to = datetime.strptime(date_end, "%Y-%m-%d")
        difference = datetime_to - datetime_from
        # return result and add a day
        return difference.days + 1

    def _prepare_analytic_line(self, date, project, sheet_id, user_id):
        return {
            "project_id": project.id,
            "amount": 0.0,
            "date": date,
            # this used to be "/", but this is now a special string considered
            # by the hr_timesheet_sheet module as an empty line. when a
            # timesheet is saved, any line with "/" as description and 0 time
            # is removed.
            "name": "-",
            "sheet_id": sheet_id,
            "unit_amount": 0,
            "user_id": user_id.id,
        }

    @api.model
    def create(self, vals):
        ts = super().create(vals)

        date_start = ts.date_start
        date_end = ts.date_end
        employee_id = ts.employee_id
        sheet_id = ts.id

        days = self.get_number_days_between_dates(date_start, date_end)
        for day in range(days):
            datetime_current = (
                datetime.strptime(date_start, "%Y-%m-%d") + timedelta(days=day)
            ).strftime("%Y-%m-%d")
            for project in employee_id.project_ids:
                aal_dict = self._prepare_analytic_line(
                    datetime_current, project, sheet_id, employee_id.user_id
                )
                ts.write({"timesheet_ids": [(0, 0, aal_dict)]})
        return ts
