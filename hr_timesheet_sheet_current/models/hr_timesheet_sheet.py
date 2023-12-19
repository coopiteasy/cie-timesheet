import datetime

from odoo import api, models
from odoo.tools.translate import _


class Sheet(models.Model):
    _inherit = "hr_timesheet.sheet"

    @api.model
    def get_current_timesheet(self):
        ts = self.env["hr_timesheet.sheet"]
        today_date = datetime.date.today()
        ids = ts.search(
            [
                ("user_id", "=", self.env.uid),
                ("state", "in", ("draft", "new")),
                ("date_start", "<=", today_date),
                ("date_end", ">=", today_date),
            ]
        )
        view_type = "form,tree"

        context = self.env.context
        action = {
            "name": _("Open Timesheet"),
            "view_type": "form",
            "view_mode": view_type,
            "res_model": "hr_timesheet.sheet",
            "view_id": False,
            "type": "ir.actions.act_window",
            "context": context,
            "domain": "[('user_id', '=', uid)]",
            "res_id": ids.id,
        }
        return action
