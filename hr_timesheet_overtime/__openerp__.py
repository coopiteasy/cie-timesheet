# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Timesheet/Contract - Overtime",
    "version": "9.0.1.0.0",
    "category": "Human Resources",
    "summary": """Overtime Calculation""",
    "description": """Computes overtime hours according to employee's contracts""",
    "author": "Coop IT Easy SCRLfs, Odoo Community Association (OCA)",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["hr_contract", "hr_timesheet_sheet"],
    "data": [
        "views/hr_timesheet_sheet_view.xml",
        "views/hr_employee_view.xml",
    ],
    "demo": ["demo/hr_contract_demo.xml"],
    "installable": True,
}
