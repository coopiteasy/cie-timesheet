# Copyright 2021 Victor Champonnois
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Hr Timesheet Current',
    'description': """
        Adds "my current timsheet" menu and open it directly when selecting the Timesheet menu""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Coop IT Easy SCRLfs',
    'depends': [
        'hr_timesheet',
        'hr_timesheet_sheet',
    ],
    'data': [
        "wizard/hr_timesheet_current_view.xml",
        "views/my_current_view.xml"
    ],
    'demo': [
    ],
}
