# -*- coding: utf-8 -*-
# Copyright 2016 Sunflower IT <http://sunflowerweb.nl>
# Copyright 2019 Coop IT Easy SCRLfs
#   - Vincent Van Rossem <vincent@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    # touch
    "name": "Link holidays to analytic lines",
    "version": "9.0.1.0.0",
    "category": "Generic Modules/Human Resources",
    "summary": """When holidays are granted, add lines to the analytic account
        that is linked to the Leave Type""",
    "author": "Coop IT Easy SCRLfs, "
    "Sunflower IT, Therp BV, "
    "Odoo Community Association (OCA)",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": ["hr_holidays", "hr_timesheet_sheet", "hr_contract"],
    "data": ["views/hr_holidays_view.xml", "views/company_view.xml"],
    "installable": True,
}
