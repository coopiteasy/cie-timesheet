# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp import exceptions


class TestOvertime(TransactionCase):
    def setUp(self):
        super(TestOvertime, self).setUp()
        # users
        user1_dict = {"name": "User 1", "login": "user1", "password": "user1"}
        self.user1 = self.env["res.users"].create(user1_dict)

        # employees
        employee1_dict = {
            "name": "Employee 1",
            "user_id": self.user1.id,
            "address_id": self.user1.partner_id.id,
            "overtime_start_date": "2019-01-01",
        }
        self.employee1 = self.env["hr.employee"].create(employee1_dict)

        # working hours
        calendar = self.env["resource.calendar"].create({"name": "Calendar"})
        for day in range(5):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": "09",
                    "hour_to": "18",
                    "calendar_id": calendar[0].id,
                }
            )

        # contracts
        contract_dict = {
            "name": "Contract 1",
            "employee_id": self.employee1.id,
            "wage": 0.0,
            "working_hours": calendar.id,
        }

        self.contract1 = self.env["hr.contract"].create(contract_dict)

        # analytic accounts
        self.analytic_account_01 = self.env["account.analytic.account"].create(
            {"name": "Analytic Account 01"}
        )

        # create ts
        ts1_dict = {
            "employee_id": self.employee1.id,
            "date_from": "2019-12-02",
            "date_to": "2019-12-08",
        }
        self.ts1 = self.env["hr_timesheet_sheet.sheet"].create(ts1_dict)

        # create and link aal
        self.env["account.analytic.line"].create(
            {
                "account_id": self.analytic_account_01.id,
                "amount": 0.0,
                "date": "2019-12-02",
                "is_timesheet": "True",
                "name": "/",
                "sheet_id": self.ts1.id,
                "unit_amount": 10.0,
                "user_id": self.employee1.user_id.id,
            }
        )

    def test_overtime_01(self):
        """
        A timesheet and its analytic line with one hour extra time
        """

        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 1)

    def test_overtime_02(self):
        """
        Change overtime start date
        """
        self.employee1.write({"overtime_start_date": "2019-12-09"})

        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 0)

    def test_overtime_03(self):
        """
        Change initial overtime
        """
        self.employee1.write({"initial_overtime": 10})

        self.assertEqual(self.ts1.timesheet_overtime, 1)
        self.assertEqual(self.ts1.total_overtime, 11)
