# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api, fields


class ResourceOvertimeRate(models.Model):
    _name = "resource.overtime.rate"
    _description = "Rate detail"
    _order = "dayofweek"

    # String fields
    name = fields.Char(required=True)
    dayofweek = fields.Selection(
        [
            ("0", "Monday"),
            ("1", "Tuesday"),
            ("2", "Wednesday"),
            ("3", "Thursday"),
            ("4", "Friday"),
            ("5", "Saturday"),
            ("6", "Sunday"),
        ],
        "Day of Week",
        required=True,
        index=True,
    )

    # Numeric fields
    rate = fields.Float("Rate", default="1.00", digits=(3, 2))
    overtime_id = fields.Many2one(
        "resource.overtime",
        string="Resource's Overtime",
        required=True,
        ondelete="cascade",
    )
