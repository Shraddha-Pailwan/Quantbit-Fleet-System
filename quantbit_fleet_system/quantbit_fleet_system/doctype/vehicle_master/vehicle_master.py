# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

# Copyright (c) 2026, Quantbit

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today, add_days

class VehicleMaster(Document):
    def validate(self):
        self.update_document_status()

    def update_document_status(self):
        current_date = getdate(today())
        for row in self.vehicle_document:
            if not row.expiry_date:
                row.status = "Valid"
                continue
            expiry_date = getdate(row.expiry_date)
            reminder_days = int(row.renewal_reminder_days or 0)
            reminder_date = add_days(expiry_date, -reminder_days)
            if current_date > expiry_date:
                row.status = "Expired"
            elif current_date >= reminder_date:
                row.status = "Pending Renewal"
            else:
                row.status = "Valid"

