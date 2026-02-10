# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class FuelEntry(Document):
    def before_insert(self):
        if not self.posting_date:
            self.posting_date = nowdate()

    def validate(self):
        self.fetch_driver_from_vehicle()
        self.validate_basic()
        self.calculate_total()

    def fetch_driver_from_vehicle(self):
        if not self.vehicle:
            return
        assignment = frappe.db.get_list(
            "Vehicle Assignment",
            filters={
                "vehicle": self.vehicle,
                "status": "Active",
                "docstatus": ["<", 2]
            },
            fields=["driver"],
            order_by="modified desc",
            limit=1
        )
        if assignment and not self.driver:
            self.driver = assignment[0].driver

    def validate_basic(self):
        if not self.vehicle:
            frappe.throw("Vehicle is mandatory")
        if not self.quantity_liters or self.quantity_liters <= 0:
            frappe.throw("Fuel quantity must be greater than 0")
        if not self.rate_per_liter or self.rate_per_liter <= 0:
            frappe.throw("Rate per liter must be greater than 0")
        if self.odometer_reading and self.odometer_reading < 0:
            frappe.throw("Odometer reading cannot be negative")
        if self.posting_date:
            if getdate(self.posting_date) > getdate(nowdate()):
                frappe.throw("Posting Date cannot be in future")

    def calculate_total(self):
        qty = self.quantity_liters or 0
        rate = self.rate_per_liter or 0
        self.total_amount = qty * rate

