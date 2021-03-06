# -*- coding: utf-8 -*-
# Copyright 2016 Sunflower IT <http://sunflowerweb.nl>
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class AnalyticLine(models.Model):
    """Restrict edit and delete on analytic lines generated by holidays"""

    _inherit = "account.analytic.line"

    leave_id = fields.Many2one(comodel_name="hr.holidays", string="Leave id")

    @api.multi
    def write(self, vals):
        if not self.env.context.get("force_write", False):
            for rec in self:
                if rec.account_id.is_leave_account and rec.leave_id:
                    raise ValidationError(
                        _(
                            "This line is protected against editing because it "
                            "was created automatically by a leave request. "
                            "Please edit the leave request instead."
                        )
                    )
        super(AnalyticLine, self).write(vals)
