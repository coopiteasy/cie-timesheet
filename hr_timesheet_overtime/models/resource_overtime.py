# Copyright 2020 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResourceOvertime(models.Model):
    _name = "resource.overtime"
    _description = "Resource Overtime"

    # String fields
    name = fields.Char(required=True)

    # Relational fields
    rate_ids = fields.One2many(
        comodel_name="resource.overtime.rate",
        inverse_name="overtime_id",
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
