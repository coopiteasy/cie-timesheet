Handle the links between sale order lines and timesheets when changing the
project of a timesheet of a task.

If the project of timesheet is equal to the project of the task to which it is
linked, then the timesheet is linked to the sale order line of the task
(possibly null).

If the project of timesheet is not equal to the project of the task to which
it is linked, then the timesheet is linked to the sale order line of the
project (possibly null).

Note: this module ignores the ``billable_type`` project and task properties,
assuming it is always equal to ``"task_rate"``.
