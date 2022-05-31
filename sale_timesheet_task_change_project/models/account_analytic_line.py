# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    @api.multi
    def write(self, vals):
        result = True
        for rec in self:
            # the sale order line depends on the task and the project, so it can be
            # different for each rec and must be computed individually.
            rec_vals = vals.copy()
            self._adjust_so_line_link_write_vals(rec, rec_vals)
            # it must be an explicit super(), because it must be run on rec, not self.
            result = super(AccountAnalyticLine, rec).write(rec_vals) and result
        return result

    def _adjust_so_line_link_write_vals(self, rec, vals):
        # adjust vals["so_line"] according to the project and the task.
        project = rec.project_id
        if not project and not vals.get("project_id"):
            # not a timesheet
            return
        if "project_id" in vals:
            project = self.env["project.project"].browse(vals["project_id"])
        if "task_id" in vals:
            task = self.env["project.task"].browse(vals["task_id"])
        else:
            task = rec.task_id
        if "so_line" in vals:
            so_line = self.env["sale.order.line"].browse(vals["so_line"])
        else:
            so_line = rec.so_line
        if task:
            if project == task.project_id:
                if so_line == task.sale_line_id:
                    return
                vals["so_line"] = task.sale_line_id.id
                return
        if project.sale_line_id:
            if so_line == project.sale_line_id:
                return
            vals["so_line"] = project.sale_line_id.id
            return
        if so_line:
            vals["so_line"] = False
