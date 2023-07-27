# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Prevent creation of projects and tasks from timesheets",
    "summary": """
        Prevent creation of projects and tasks from timesheets.""",
    "version": "14.0.1.0.0",
    "category": "Human Resources",
    "website": "https://github.com/coopiteasy/cie-timesheet",
    "author": "Coop IT Easy SC",
    "maintainers": ["carmenbianca"],
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr_timesheet",
        "hr_timesheet_sheet",
    ],
    "excludes": [],
    "data": [
        "views/hr_timesheet_sheet_views.xml",
        "views/hr_timesheet_views.xml",
    ],
    "demo": [],
    "qweb": [],
}
