# -*- coding: utf-8 -*-
# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from openerp import api, models

from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class HrTimesheetSheet(models.Model):
    _inherit = "hr_timesheet_sheet.sheet"

    @api.model
    def create_employee_timesheet(self):
        _logger.info("[hr_timesheet_auto_creation][create_employee_timesheet]")
        employee_obj = self.env["hr.employee"]
        employee_ids = employee_obj.search(
            [("active", "=", True), ("user_id", "!=", False)]
        ).ids
        today = datetime.now()
        monday = today + timedelta(days=-today.weekday())
        sunday = monday + timedelta(days=+6)
        # Search for existing timesheet
        exists_timesheet_records = self.search([("date_to", ">=", monday)])
        ignore_employee_ids = map(
            lambda x: x.employee_id.id, exists_timesheet_records
        )
        employee_ids = list(set(employee_ids) - set(ignore_employee_ids))
        vals = {
            "date_from": monday.strftime("%Y-%m-%d"),
            "date_to": sunday.strftime("%Y-%m-%d"),
        }
        for employee_id in employee_ids:
            vals["employee_id"] = employee_id
            self.sudo().create(vals)
            _logger.info(
                "[hr_timesheet_auto_creation] hr_timesheet_sheet.sheet created for employee %s"
                % employee_id
            )

        return True


class Followers(models.Model):
    _inherit = "mail.followers"

    @api.model
    def create(self, vals):
        """
        Fix for IntegrityError: duplicate key value violates unique constraint
            "mail_followers_mail_followers_res_partner_res_model_id_uniq"
        Found on https://github.com/odoo/odoo/issues/15589#issuecomment-455635940
        """
        if "res_model" in vals and "res_id" in vals and "partner_id" in vals:
            dups = self.env["mail.followers"].search(
                [
                    ("res_model", "=", vals.get("res_model")),
                    ("res_id", "=", vals.get("res_id")),
                    ("partner_id", "=", vals.get("partner_id")),
                ]
            )
            if len(dups):
                for p in dups:
                    p.unlink()
        res = super(Followers, self).create(vals)
        return res
