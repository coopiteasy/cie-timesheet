import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class AnalyticLine(models.Model):
    """
    Apply on account analytic lines the rate defined in resource.overtime.rate
    """

    _inherit = "account.analytic.line"

    @api.model
    def create(self, values):
        self._update_values(values)
        return super(AnalyticLine, self).create(values)

    @api.multi
    def write(self, values):
        self._update_values(values)
        return super(AnalyticLine, self).write(values)

    @api.model
    def _update_values(self, values):
        if values.get("date") or values.get("unit_amount"):
            date = values.get("date")
            unit_amount = values.get("unit_amount", self.unit_amount)

            # rate management
            weekday = fields.Date.from_string(date).weekday()
            rate = (
                self.env["resource.overtime.rate"]
                .search([("dayofweek", "=", weekday)], limit=1)
                .rate
                or 1.0
            )

            # update
            values["unit_amount"] = unit_amount * rate
