# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class VehicleExpense(Document):
    def before_insert(self):
        if not self.payment_status:
            self.payment_status = "Pending"

    def validate(self):
        self.validate_dates()
        self.validate_amount()
        self.validate_odometer()
        self.validate_accounts()
        self.fetch_driver_from_assignment()

    def validate_dates(self):
        if self.expense_date:
            expense_date = getdate(self.expense_date)
            current_date = getdate(today())
            if expense_date > current_date:
                frappe.throw("Expense Date cannot be in future")

    def validate_amount(self):
        if not self.amount or self.amount <= 0:
            frappe.throw("Amount must be greater than 0")

    def validate_odometer(self):
        if self.odometer_reading is None:
            return
        if self.odometer_reading < 0:
            frappe.throw("Odometer reading cannot be negative")

    def validate_accounts(self):
        if not self.account:
            frappe.throw("Expense Account is mandatory")
        if not self.payment_account:
            frappe.throw("Payment Account is mandatory")

    def fetch_driver_from_assignment(self):
        if not self.vehicle or self.driver:
            return
        assignment = frappe.db.get_value(
            "Vehicle Assignment",
            {
                "vehicle": self.vehicle,
                "status": "Active",
                "docstatus": ["<", 2]
            },
            ["driver"],
            order_by="modified desc"
        )
        if assignment:
            self.driver = assignment

