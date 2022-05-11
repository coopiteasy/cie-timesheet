# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    @api.constrains("task_id", "project_id")
    def _check_task_project(self):
        # in the hr_timesheet module, this method is a constraint on task_id
        # and project_id to ensure that the task to which the account analytic
        # line is linked is linked to the same project. this override removes
        # this constraint.
        pass

    @api.onchange("project_id")
    def onchange_project_id(self):
        # in the hr_timesheet module, this method sets task_id to False if the
        # selected project is not the task's project. this override removes
        # this behavior.
        task_id = self.task_id
        # the parent method returns a domain to limit the available tasks, so
        # it needs to be returned.
        result = super().onchange_project_id()
        if task_id:
            self.task_id = task_id
        return result
