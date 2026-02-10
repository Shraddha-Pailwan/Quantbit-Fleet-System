# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class TripRequest(Document):
    def before_insert(self):
        self.trip_request_status = "Requested"

    def validate(self):
        self.validate_dates()

    def validate_dates(self):
        if self.expected_trip_start_date and self.expected_trip_end_date:
            if self.expected_trip_start_date > self.expected_trip_end_date:
                frappe.throw("Expected Start Date cannot be after End Date")