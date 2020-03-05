# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, api, fields


class ResourceOvertime(models.Model):
    _name = "resource.overtime"
    _description = "Resource Overtime"

    # String fields
    name = fields.Char(required=True)

    # Relational fields
    rate_ids = fields.One2many(
        "resource.overtime.rate",
        "overtime_id",
        string="Overtime Rate",
        copy=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env["res.company"]._company_default_get(),
    )
    manager = fields.Many2one(
        "res.users",
        string="Workgroup Manager",
        default=lambda self: self.env.uid,
    )
