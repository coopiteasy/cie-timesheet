# Copyright 2020 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date

from odoo.tests.common import TransactionCase


class TestOvertime(TransactionCase):
    def setUp(self):
        super().setUp()
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
        # calendar have default attendance_ids, force it to have none.
        calendar = self.env["resource.calendar"].create(
            {"name": "Calendar", "attendance_ids": False}
        )
        for day in range(5):
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 9.0,
                    "hour_to": 18.0,
                    "calendar_id": calendar[0].id,
                }
            )

        # contracts
        contract_dict = {
            "name": "Contract 1",
            "employee_id": self.employee1.id,
            "wage": 0.0,
            "resource_calendar_id": calendar.id,
            "date_start": "2019-01-01",
        }

        self.contract1 = self.env["hr.contract"].create(contract_dict)

        # projects
        self.project_01 = self.env["project.project"].create({"name": "Project 01"})

        # create ts
        ts1_dict = {
            "employee_id": self.employee1.id,
            "date_start": "2019-12-02",
            "date_end": "2019-12-08",
        }
        self.ts1 = self.env["hr_timesheet.sheet"].create(ts1_dict)

        # create and link aal
        # monday 02/12/2019
        self.env["account.analytic.line"].create(
            {
                "project_id": self.project_01.id,
                "amount": 0.0,
                "date": "2019-12-02",
                "name": "-",
                "sheet_id": self.ts1.id,
                "unit_amount": 10.0,  # 1 hour overtime
                "user_id": self.employee1.user_id.id,
            }
        )
        # tuesday 03/12/2019 -> friday 06/12/2019
        for day in range(3, 7):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": self.ts1.id,
                    "unit_amount": 9.0,  # expected time
                    "user_id": self.employee1.user_id.id,
                }
            )

    def test_overtime_01(self):
        """
        A timesheet and its analytic line with one hour extra time
        """

        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.total_overtime, 1)

    def test_overtime_02(self):
        """
        Change overtime start date
        """
        ts2 = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee1.id,
                "date_start": "2019-12-09",
                "date_end": "2019-12-15",
            }
        )

        # create and link aal
        # monday and tuesday
        for day in range(9, 11):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 10.0,  # 1 hour overtime
                    "user_id": self.employee1.user_id.id,
                }
            )
        # wednesday -> thursday
        for day in range(10, 13):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 9.0,  # expected time
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.employee1.write({"overtime_start_date": "2019-12-10"})

        # overtime for any timesheet takes overtime_start_date into account
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 0)
        # it should start computing on tuesday
        self.assertEqual(ts2.timesheet_overtime_trimmed, 1)
        self.assertEqual(ts2.total_overtime, 1)
        # total_overtime is just a link to the employee's total overtime
        self.assertEqual(self.ts1.total_overtime, 1)

    def test_overtime_03(self):
        """
        Change initial overtime
        """
        self.employee1.write({"initial_overtime": 10})

        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.total_overtime, 11)

    def test_overtime_04(self):
        """
        Worker did not work on a day he was expected to work on.
        """
        ts2 = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee1.id,
                "date_start": "2019-12-09",
                "date_end": "2019-12-15",
            }
        )

        # create and link aal
        # monday
        self.env["account.analytic.line"].create(
            {
                "project_id": self.project_01.id,
                "amount": 0.0,
                "date": "2019-12-09",
                "name": "-",
                "sheet_id": ts2.id,
                "unit_amount": 10.0,  # 1 hour overtime
                "user_id": self.employee1.user_id.id,
            }
        )
        # tuesday -> thursday
        for day in range(10, 13):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 9.0,  # expected time
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.assertEqual(ts2.timesheet_overtime_trimmed, -8)
        self.assertEqual(ts2.total_overtime, -7)

    def test_overtime_05(self):
        """
        Multiple contracts
        """

        # end previous contract
        self.contract1.date_end = "2020-01-06"

        # create new contract
        # working hours : half-time
        calendar = self.env["resource.calendar"].create(
            {"name": "Calendar", "attendance_ids": False}
        )
        for day in range(5):  # from monday to friday
            self.env["resource.calendar.attendance"].create(
                {
                    "name": "Attendance",
                    "dayofweek": str(day),
                    "hour_from": 9.0,
                    "hour_to": 13.0,
                    "calendar_id": calendar[0].id,
                }
            )

        # contracts
        contract_dict = {
            "name": "Contract 2",
            "employee_id": self.employee1.id,
            "wage": 0.0,
            "resource_calendar_id": calendar.id,
            "date_start": "2020-01-07",
        }

        self.contract2 = self.env["hr.contract"].create(contract_dict)

        # create ts
        ts2_dict = {
            "employee_id": self.employee1.id,
            "date_start": "2020-01-06",
            "date_end": "2020-01-12",
        }
        self.ts2 = self.env["hr_timesheet.sheet"].create(ts2_dict)

        # create and link aal
        # monday
        self.env["account.analytic.line"].create(
            {
                "project_id": self.project_01.id,
                "amount": 0.0,
                "date": "2020-01-06",
                "name": "-",
                "sheet_id": self.ts2.id,
                "unit_amount": 9.0,  # expected time from previous contract
                "user_id": self.employee1.user_id.id,
            }
        )

        # tuesday 07/01/2020 -> friday 10/01/2020
        for day in range(7, 11):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2020, 1, day),
                    "name": "-",
                    "sheet_id": self.ts2.id,
                    "unit_amount": 4.0,  # expected time from new contract
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.assertEqual(self.ts2.timesheet_overtime_trimmed, 0)
        self.assertEqual(self.ts2.total_overtime, 1)  # 1 hour overtime from ts1

    def test_overtime_archived_timesheet(self):
        """
        Archived timesheets
        """
        ts2 = self.env["hr_timesheet.sheet"].create(
            {
                "employee_id": self.employee1.id,
                "date_start": "2019-12-09",
                "date_end": "2019-12-15",
            }
        )

        # create and link aal
        # monday -> friday
        for day in range(9, 14):
            self.env["account.analytic.line"].create(
                {
                    "project_id": self.project_01.id,
                    "amount": 0.0,
                    "date": date(2019, 12, day),
                    "name": "-",
                    "sheet_id": ts2.id,
                    "unit_amount": 10.0,  # 1 hour overtime
                    "user_id": self.employee1.user_id.id,
                }
            )

        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.total_overtime, 6)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.total_overtime, 6)
        self.assertEqual(self.employee1.total_overtime, 6)

        self.ts1.write({"active": False})
        # an inactive timesheet still has the same overtime
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.total_overtime, 5)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.total_overtime, 5)
        self.assertEqual(self.employee1.total_overtime, 5)

        ts2.write({"active": False})
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.total_overtime, 0)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.total_overtime, 0)
        self.assertEqual(self.employee1.total_overtime, 0)

        self.ts1.write({"active": True})
        self.assertEqual(self.ts1.timesheet_overtime_trimmed, 1)
        self.assertEqual(self.ts1.total_overtime, 1)
        self.assertEqual(ts2.timesheet_overtime_trimmed, 5)
        self.assertEqual(ts2.total_overtime, 1)
        self.assertEqual(self.employee1.total_overtime, 1)
