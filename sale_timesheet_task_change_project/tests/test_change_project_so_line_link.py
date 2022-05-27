# Copyright 2022 Coop IT Easy SCRLfs
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestChangeProjectSOLineLink(TransactionCase):
    def setUp(self):
        super().setUp()

        # partners
        partner1_dict = {"name": "partner1"}
        self.partner1 = self.env["res.partner"].create(partner1_dict)

        # products
        product1_dict = {"name": "product1", "type": "service"}
        self.product1 = self.env["product.product"].create(product1_dict)

        # sale orders
        so1_dict = {"name": "so1", "partner_id": self.partner1.id}
        self.so1 = self.env["sale.order"].create(so1_dict)
        so2_dict = {"name": "so2", "partner_id": self.partner1.id}
        self.so2 = self.env["sale.order"].create(so2_dict)
        so3_dict = {"name": "so3", "partner_id": self.partner1.id}
        self.so3 = self.env["sale.order"].create(so3_dict)

        # sale order lines
        uom_hour = self.env.ref("uom.product_uom_hour")
        sol1_1_dict = {
            "name": "sol1_1",
            "order_id": self.so1.id,
            "product_id": self.product1.id,
            "product_uom": uom_hour.id,
        }
        self.sol1_1 = self.env["sale.order.line"].create(sol1_1_dict)
        sol1_2_dict = {
            "name": "sol1_2",
            "order_id": self.so1.id,
            "product_id": self.product1.id,
            "product_uom": uom_hour.id,
        }
        self.sol1_2 = self.env["sale.order.line"].create(sol1_2_dict)
        sol1_3_dict = {
            "name": "sol1_3",
            "order_id": self.so1.id,
            "product_id": self.product1.id,
            "product_uom": uom_hour.id,
        }
        self.sol1_3 = self.env["sale.order.line"].create(sol1_3_dict)
        sol2_1_dict = {
            "name": "sol2_1",
            "order_id": self.so2.id,
            "product_id": self.product1.id,
            "product_uom": uom_hour.id,
        }
        self.sol2_1 = self.env["sale.order.line"].create(sol2_1_dict)
        sol2_2_dict = {
            "name": "sol2_1",
            "order_id": self.so2.id,
            "product_id": self.product1.id,
            "product_uom": uom_hour.id,
        }
        self.sol2_2 = self.env["sale.order.line"].create(sol2_2_dict)

        # projects
        project1_dict = {
            "name": "project1",
            "allow_timesheets": True,
            "sale_order_id": self.so1.id,
            "sale_line_id": self.sol1_2.id,
        }
        self.project1 = self.env["project.project"].create(project1_dict)
        project2_dict = {
            "name": "project2",
            "allow_timesheets": True,
            "sale_order_id": self.so2.id,
            "sale_line_id": self.sol2_2.id,
        }
        self.project2 = self.env["project.project"].create(project2_dict)
        project3_dict = {"name": "project3", "allow_timesheets": True}
        self.project3 = self.env["project.project"].create(project3_dict)
        project4_dict = {
            "name": "project4",
            "allow_timesheets": True,
            "sale_order_id": self.so2.id,
        }
        self.project4 = self.env["project.project"].create(project4_dict)
        project5_dict = {
            "name": "project5",
            "allow_timesheets": True,
            "sale_order_id": self.so3.id,
        }
        self.project5 = self.env["project.project"].create(project5_dict)

        # users
        user1_dict = {"name": "User 1", "login": "user1", "password": "user1"}
        self.user1 = self.env["res.users"].create(user1_dict)

        # employees
        employee1_dict = {
            "name": "employee1",
            "user_id": self.user1.id,
        }
        self.employee1 = self.env["hr.employee"].create(employee1_dict)

    def test_create_with_project_without_so(self):
        activity = self._create_activity(self.project3)
        self.assertFalse(activity.so_line)

    def test_create_with_project_with_so_with_so_lines(self):
        activity = self._create_activity(self.project4)
        self.assertFalse(activity.so_line)

    def test_create_with_project_with_so_without_so_lines(self):
        activity = self._create_activity(self.project5)
        self.assertFalse(activity.so_line)

    def test_create_with_project_with_so_line(self):
        activity = self._create_activity(self.project1)
        self.assertEqual(activity.so_line, self.sol1_2)

    def test_create_with_task_with_project_without_so(self):
        task = self._create_task(self.project3)
        activity = self._create_activity(self.project3, task)
        self.assertFalse(activity.so_line)

    def test_create_with_task_with_project_with_so_with_so_lines(self):
        task = self._create_task(self.project4)
        # the task so_line comes from the project, so it is null
        self.assertFalse(task.sale_line_id)
        activity = self._create_activity(self.project4, task)
        self.assertFalse(activity.so_line)

    def test_create_with_task_with_project_with_so_without_so_lines(self):
        task = self._create_task(self.project5)
        activity = self._create_activity(self.project5, task)
        self.assertFalse(activity.so_line)

    def test_create_with_task_with_project_with_so_line(self):
        task = self._create_task(self.project1)
        # the task so_line comes from the project
        self.assertEqual(task.sale_line_id, self.sol1_2)
        activity = self._create_activity(self.project1, task)
        self.assertEqual(activity.so_line, self.sol1_2)

    def test_create_with_task_with_so_line(self):
        task = self._create_task(self.project1, self.sol1_3)
        activity = self._create_activity(self.project1, task)
        self.assertEqual(activity.so_line, self.sol1_3)

    def test_create_with_task_with_other_project_without_so(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project3, task)
        self.assertFalse(activity.so_line)

    def test_create_with_task_with_other_project_with_so_with_so_lines(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project4, task)
        self.assertFalse(activity.so_line)

    def test_create_with_task_with_other_project_with_so_without_so_lines(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project5, task)
        self.assertFalse(activity.so_line)

    def test_create_with_task_with_other_project_with_so_line(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project2, task)
        self.assertEqual(activity.so_line, self.sol2_2)

    def test_change_to_project_with_so_line(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project1, task)
        activity.project_id = self.project2
        self.assertEqual(activity.so_line, self.sol2_2)

    def test_change_to_project_without_so(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project1, task)
        activity.project_id = self.project3
        self.assertFalse(activity.so_line)

    def test_change_to_project_with_so_with_so_lines(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project1, task)
        activity.project_id = self.project4
        self.assertFalse(activity.so_line)

    def test_change_to_project_with_so_without_so_lines(self):
        task = self._create_task(self.project1)
        activity = self._create_activity(self.project1, task)
        activity.project_id = self.project5
        self.assertFalse(activity.so_line)

    def test_change_to_task_with_so_line(self):
        activity = self._create_activity(self.project1)
        self.assertEqual(activity.so_line, self.sol1_2)
        task = self._create_task(self.project1, self.sol1_3)
        activity.task_id = task
        self.assertEqual(activity.so_line, self.sol1_3)

    def test_change_to_project_and_task_with_so_line(self):
        activity = self._create_activity(self.project2)
        self.assertEqual(activity.so_line, self.sol2_2)
        task = self._create_task(self.project1, self.sol1_3)
        activity.write({"project_id": self.project1.id, "task_id": task.id})
        self.assertEqual(activity.project_id, self.project1)
        self.assertEqual(activity.so_line, self.sol1_3)

    def test_change_to_task_with_so_line_but_other_project(self):
        activity = self._create_activity(self.project2)
        self.assertEqual(activity.so_line, self.sol2_2)
        task = self._create_task(self.project1)
        activity.task_id = task
        # since the project is not the same as the one of the task, the
        # so_line comes from the project.
        self.assertEqual(activity.project_id, self.project2)
        self.assertEqual(activity.so_line, self.sol2_2)

    def test_change_to_task_with_other_so_line_and_other_project(self):
        activity = self._create_activity(self.project3)
        task = self._create_task(self.project1, self.sol1_3)
        activity.task_id = task
        # since the project is not the same as the one of the task, the
        # so_line comes from the project.
        self.assertEqual(activity.project_id, self.project3)
        self.assertFalse(activity.so_line)

    def test_change_back_to_project_task_with_so_line(self):
        task = self._create_task(self.project1, self.sol1_3)
        activity = self._create_activity(self.project2, task)
        self.assertEqual(activity.so_line, self.sol2_2)
        activity.project_id = self.project1
        self.assertEqual(activity.so_line, self.sol1_3)

    def test_change_back_to_project_task_without_so_line(self):
        task = self._create_task(self.project1)
        task.sale_line_id = False
        activity = self._create_activity(self.project2, task)
        self.assertEqual(activity.so_line, self.sol2_2)
        activity.project_id = self.project1
        self.assertFalse(activity.so_line)

    def test_change_to_task_and_other_project_without_so(self):
        activity = self._create_activity(self.project2)
        task = self._create_task(self.project1)
        activity.write({"project_id": self.project3.id, "task_id": task.id})
        self.assertFalse(activity.so_line)

    def test_change_to_task_and_other_project_with_so_with_so_lines(self):
        activity = self._create_activity(self.project2)
        task = self._create_task(self.project1)
        activity.write({"project_id": self.project4.id, "task_id": task.id})
        self.assertFalse(activity.so_line)

    def test_change_to_task_and_other_project_with_so_without_so_lines(self):
        activity = self._create_activity(self.project2)
        task = self._create_task(self.project1)
        activity.write({"project_id": self.project5.id, "task_id": task.id})
        self.assertFalse(activity.so_line)

    def test_change_to_task_and_other_project_with_so_line(self):
        activity = self._create_activity(self.project3)
        task = self._create_task(self.project1)
        activity.write({"project_id": self.project2.id, "task_id": task.id})
        self.assertEqual(activity.so_line, self.sol2_2)

    def _create_task(self, project, so_line=None):
        task_dict = {"name": "task1", "project_id": project.id}
        if so_line:
            task_dict["sale_line_id"] = so_line.id
        return self.env["project.task"].create(task_dict)

    def _create_activity(self, project=None, task=None):
        activity_dict = {
            "name": "activity",
            "unit_amount": 1.0,
            "employee_id": self.employee1.id,
        }
        if project:
            activity_dict["project_id"] = project.id
        if task:
            activity_dict["task_id"] = task.id
        return self.env["account.analytic.line"].create(activity_dict)
