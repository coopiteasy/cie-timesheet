# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    cr = env.cr

    # employees are now linked to projects instead of analytic accounts. since
    # a project was automatically created for each analytic account, we link
    # the corresponding projects using the old relationship table.
    openupgrade.logged_query(
        cr,
        """
        insert into hr_employee_project_project_rel
        select hr_employee_id, project.id
        from account_analytic_account_hr_employee_rel as aa_e
        inner join project_project as project
        on project.analytic_account_id = aa_e.account_analytic_account_id
        """,
    )
    openupgrade.logged_query(
        cr,
        """
        drop table account_analytic_account_hr_employee_rel
        """,
    )

    # "/" is now a special string considered by the hr_timesheet_sheet module
    # as an empty line. when a timesheet is saved, any line with "/" as
    # description and 0 time is removed. use "-" instead.
    openupgrade.logged_query(
        cr,
        """
        update account_analytic_line
        set name = '-' where name = '/'
        """,
    )
