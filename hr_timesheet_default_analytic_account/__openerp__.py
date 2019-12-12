# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Default analytic accounts upon timesheet creation",
    "version": "9.0.1.0.0",
    "category": "Human Resources",
    "summary": """
    When creating a timesheet, adds for the period analytical lines linked to an employee's default analytic accounts
    """,
    "author": "Coop IT Easy SCRLfs, Odoo Community Association (OCA)",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["hr_timesheet_sheet"],
    "data": ["views/hr_employee_view.xml"],
    "demo": ["demo/default_analytic_account_demo.xml"],
    "installable": True,
}
