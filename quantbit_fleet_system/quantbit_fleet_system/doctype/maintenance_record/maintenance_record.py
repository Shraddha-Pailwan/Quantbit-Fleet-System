# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class MaintenanceRecord(Document):
    def before_insert(self):
        if not self.status:
            self.status = "Scheduled"

    def validate(self):
        self.calculate_total_cost()
        self.update_status()
        self.validate_basic()

    def calculate_total_cost(self):
        labor = self.labor_charges or 0
        parts = self.parts_cost or 0
        self.total_cost = labor + parts

    def update_status(self):
        today = getdate(nowdate())
        if self.docstatus == 1:
            self.status = "Completed"
            return
        if self.service_date:
            service_date = getdate(self.service_date)
            if service_date <= today:
                self.status = "In Progress"
            else:
                self.status = "Scheduled"

    def validate_basic(self):
        if not self.vehicle:
            frappe.throw("Vehicle is mandatory")
        if self.labor_charges and self.labor_charges < 0:
            frappe.throw("Labor Charges cannot be negative")
        if self.parts_cost and self.parts_cost < 0:
            frappe.throw("Parts Cost cannot be negative")
        if self.odometer_reading and self.odometer_reading < 0:
            frappe.throw("Odometer Reading cannot be negative")

