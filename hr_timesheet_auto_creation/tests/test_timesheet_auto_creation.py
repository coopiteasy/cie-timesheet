# © 2016-2017 Elico Corp (https://www.elico-corp.com)
# Copyright 2019 Coop IT Easy SC
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import date, timedelta

from odoo.tests import common


class TestHrTimesheetSheet(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["hr.employee"].search([]).write({"user_id": False})
        cls.tms_obj = cls.env["hr_timesheet.sheet"]
        today = date.today()
        cls.monday = today + timedelta(days=-today.weekday())
        cls.sunday = cls.monday + timedelta(days=6)

        cls.user1 = cls.env.ref("base.user_root").copy({"login": "test1"})
        cls.employee1 = cls.env.ref("hr.employee_ngh")
        cls.employee1.user_id = cls.user1.id

        cls.user2 = cls.user1.copy({"login": "test2"})
        cls.employee2 = cls.env.ref("hr.employee_vad").copy({"user_id": cls.user2.id})

    def test_create_employee_timesheet(self):
        """Check timesheet has been created automatically for the week."""
        conditions = [
            ("employee_id", "in", (self.employee1.id, self.employee2.id)),
            ("date_start", "=", self.monday),
            ("date_end", "=", self.sunday),
        ]
        # test that no matching timesheets exist yet.
        tms = self.tms_obj.search(conditions)
        self.assertEqual(len(tms), 0)
        self.tms_obj.create_employee_timesheet()
        # test that the timesheets have correctly been created.
        tms = self.tms_obj.search(conditions)
        self.assertEqual(len(tms), 2)
        self.tms_obj.create_employee_timesheet()
        # test that no extra timesheets have been created, because they
        # already exist.
        tms = self.tms_obj.search(conditions)
        self.assertEqual(len(tms), 2)
