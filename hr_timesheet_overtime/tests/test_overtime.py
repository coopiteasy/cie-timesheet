# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from openerp import exceptions


class TestOvertime(TransactionCase):
    def setUp(self):
        super(TestOvertime, self).setUp()
        # models
        self.employee_model = self.env["hr.employee"]
        self.contract_model = self.env["hr.contract"]
        self.timesheet_sheet_model = self.env["hr_timesheet_sheet.sheet"]

        # refs
        self.pp_contract1 = self.env.ref("pieter_parker_contract1")
        self.pp_contract2 = self.env.ref("pieter_parker_contract2")

    def test_initial_overtime(self):
        initial_overtime = self.timesheet_sheet_model._get_initial_overtime()
        self.assertEquals(
            initial_overtime, 0.0, "Initial Overtime has a 0.0 default value"
        )
