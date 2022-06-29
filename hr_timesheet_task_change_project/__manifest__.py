# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Change Task Timesheet Project",
    "summary": "Allow to change the project of a timesheet of a task.",
    "version": "12.0.1.0.0",
    "category": "Human Resources",
    "website": "https://coopiteasy.be",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "hr_timesheet",
    ],
    "excludes": [],
    "data": [
        "views/project_task.xml",
    ],
    "demo": [],
    "qweb": [],
}
