# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, _


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet.day"

    total_overtime = fields.Float("Total Overtime Hours", readonly=True)
