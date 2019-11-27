# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from openerp import api, fields, models, _


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    # Date -> field 'name' of hr_timesheet_sheet.sheet.day
    sheet_ids = fields.One2many("hr_timesheet_sheet.sheet.day", "sheet_id", "Day", readonly=True)

    # Heures prestées / Heures d'absence
    # TODO

    # Heures à prester selon l'horaire de l'employé
    hours = fields.Float('Heures à prester', readonly=True, compute='_compute_hours')

    @api.multi
    def _compute_hours(self):

        _format = '%Y-%m-%d %H:%M:%S'
        date1 = datetime.strptime('2019-11-26 09:08:07', _format)
        today = datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')
        total = 0.0

        for contract in self.employee_id.contract_ids:
            for calendar in contract.working_hours:
                wh = calendar.get_working_hours_of_date(start_dt=date1) # returns a list ...
                print("wh = %s" % wh)

        return total



