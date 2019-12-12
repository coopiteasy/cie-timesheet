# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class TestHrTimesheetDefaultAnalyticAccount(TransactionCase):
    def setUp(self):
        super(TestHrTimesheetDefaultAnalyticAccount, self).setUp()

        # analytic accounts
        self.analytic_account_01 = self.env["account.analytic.account"].create(
            {"name": "Analytic Account 01"}
        )
        self.analytic_account_02 = self.env["account.analytic.account"].create(
            {"name": "Analytic Account 02"}
        )

    def test_timesheet_creation_fail_linked_employee(self):
        # unlinked employee
        unlinked_employee_dict = {"name": "Unlinked Employee"}
        unlinked_employee = self.env["hr.employee"].create(
            unlinked_employee_dict
        )

        ts_unlinked_employee_dict = {
            "employee_id": unlinked_employee.id,
            "date_from": "2019-12-09",
            "date_to": "2019-12-15",
        }
        with self.assertRaises(UserError):
            self.env["hr_timesheet_sheet.sheet"].create(
                ts_unlinked_employee_dict
            )

    def test_timesheet_creation_01(self):
        # user
        user_01_dict = {
            "name": "User 1",
            "login": "user1",
            "password": "password",
        }
        user_01 = self.env["res.users"].create(user_01_dict)

        # employee
        employee_01_dict = {
            "name": "Employee 1",
            "user_id": user_01.id,
            "address_id": user_01.partner_id.id,
        }
        employee_01 = (
            self.env["hr.employee"]
            .with_context(mail_create_nosubscribe=True)
            .create(employee_01_dict)
        )

        # timesheet
        ts_01_dict = {
            "employee_id": employee_01.id,
            "date_from": "2019-12-09",
            "date_to": "2019-12-15",
        }
        ts_01 = self.env["hr_timesheet_sheet.sheet"].create(ts_01_dict)

        self.assertEqual(len(ts_01.timesheet_ids), 0)

    def test_timesheet_creation_02(self):
        # user
        user_02_dict = {
            "name": "User 2",
            "login": "user2",
            "password": "password",
        }
        user_02 = self.env["res.users"].create(user_02_dict)

        # employee
        employee_02_dict = {
            "name": "Employee 2",
            "user_id": user_02.id,
            "address_id": user_02.partner_id.id,
            "analytic_account_ids": [
                (
                    6,
                    0,
                    [self.analytic_account_01.id, self.analytic_account_02.id],
                )
            ],
        }
        employee_02 = (
            self.env["hr.employee"]
            .with_context(mail_create_nosubscribe=True)
            .create(employee_02_dict)
        )

        # timesheet
        ts_02_dict = {
            "employee_id": employee_02.id,
            "date_from": "2019-12-09",
            "date_to": "2019-12-15",
        }
        ts_02 = self.env["hr_timesheet_sheet.sheet"].create(ts_02_dict)

        self.assertEqual(len(ts_02.timesheet_ids), 14)
