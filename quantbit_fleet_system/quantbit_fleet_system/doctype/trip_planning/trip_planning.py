# Copyright (c) 2026, Quantbit
# For license information, please see license.txt

import frappe
from frappe.utils import get_datetime
from frappe.model.document import Document

class TripPlanning(Document):
    def before_insert(self):
        self.plan_status = "Planned"

    def before_validate(self):
        self.fetch_from_trip_request()

    def validate(self):
        self.validate_links()
        self.validate_dates()
        self.validate_vehicle_availability()

    def on_submit(self):
        self.update_request_status()

    def on_cancel(self):
        self.reset_request_status()

    def validate_links(self):
        if not self.trip_request:
            frappe.throw("Trip Request is mandatory")
        if not frappe.db.exists("Trip Request", self.trip_request):
            frappe.throw("Invalid Trip Request")

    def validate_dates(self):
        if self.plan_start_date and self.plan_end_date:
            start = get_datetime(self.plan_start_date)
            end = get_datetime(self.plan_end_date)
            if start > end:
                frappe.throw(
                    "Plan Start Date & Time cannot be after End Date & Time"
                )

    def validate_vehicle_availability(self):
        if not self.vehicle:
            return
        conflict = frappe.db.sql("""
            SELECT name
            FROM `tabTrip Planning`
            WHERE
                vehicle = %s
                AND name != %s
                AND docstatus < 2
                AND (
                    %s <= plan_end_date
                    AND %s >= plan_start_date
                )
        """, (
            self.vehicle,
            self.name or "",
            self.plan_start_date,
            self.plan_end_date
        ))
        if conflict:
            frappe.throw(
                "Vehicle is already booked for this time slot. Please choose another time."
            )

    def update_request_status(self):
        frappe.db.set_value(
            "Trip Request",
            self.trip_request,
            "trip_request_status",
            "Assigned"
        )

    def reset_request_status(self):
        frappe.db.set_value(
            "Trip Request",
            self.trip_request,
            "trip_request_status",
            "Requested"
        )

    def fetch_from_trip_request(self):
        if not self.trip_request:
            return
        req = frappe.get_doc("Trip Request", self.trip_request)
        self.plan_start_date = req.expected_trip_start_date
        self.plan_end_date = req.expected_trip_end_date
        self.company = req.company
        if hasattr(req, "department") and req.department:
            self.from_department = req.department
        if hasattr(req, "purpose") and req.purpose:
            self.purpose = req.purpose
