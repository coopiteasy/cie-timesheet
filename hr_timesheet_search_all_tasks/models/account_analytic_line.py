# SPDX-FileCopyrightText: 2023 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import api, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.onchange("project_id")
    def _set_task_domain_on_project_change(self):
        if self.project_id:
            task_domain = [("project_id", "=", self.project_id.id)]
        else:
            task_domain = []
        return {
            "domain": {
                "task_id": task_domain,
            },
        }
