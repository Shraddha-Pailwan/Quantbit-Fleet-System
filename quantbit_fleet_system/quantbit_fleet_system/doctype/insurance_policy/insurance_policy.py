# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, add_days, getdate

class InsurancePolicy(Document):
    def before_save(self):
        self.update_policy_status()

    def update_policy_status(self):
        if not self.end_date or not self.renewal_reminder_days:
            return
        current_date = getdate(today())
        expiry_date = getdate(self.end_date)
        reminder_days = int(self.renewal_reminder_days)
        due_date = add_days(expiry_date, -reminder_days)
        if current_date >= expiry_date:
            self.policy_status = "Expired"
        elif current_date >= due_date:
            self.policy_status = "Due"
        else:
            self.policy_status = "Insured"

