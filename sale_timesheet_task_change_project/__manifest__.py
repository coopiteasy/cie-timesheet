# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Change Sales Task Timesheet Project",
    "summary": """
        Handle the links between sale order lines and timesheets when changing
        the project of a timesheet of a task.
    """,
    "version": "12.0.1.0.0",
    "category": "Hidden",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "application": False,
    "auto_install": True,
    "depends": [
        "hr_timesheet_task_change_project",
        "sale_timesheet",
    ],
    "excludes": [],
    "data": [],
    "demo": [],
    "qweb": [],
}
