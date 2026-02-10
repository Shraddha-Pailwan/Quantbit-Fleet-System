# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class TripLog(Document):
    def before_insert(self):
        if not self.trip_status:
            self.trip_status = "Planned"

    def validate(self):
        self.validate_links()
        self.fetch_from_planning()
        self.validate_dates()
        self.validate_vehicle_availability()
        self.validate_odometer()
        self.calculate_distance()

    def validate_links(self):
        if not self.trip_planning:
            frappe.throw("Trip Planning is mandatory")
        if not frappe.db.exists("Trip Planning", self.trip_planning):
            frappe.throw("Invalid Trip Planning")

    def fetch_from_planning(self):
        if not self.trip_planning:
            return
        plan = frappe.get_doc("Trip Planning", self.trip_planning)
        if not self.company:
            self.company = plan.company
        if not self.vehicle:
            self.vehicle = plan.vehicle
        if not self.driver:
            self.driver = plan.driver
        if not self.driver_name:
            self.driver_name = plan.driver_name
        if not self.start_trip_date:
            self.start_trip_date = plan.plan_start_date
        if not self.end_trip_date:
            self.end_trip_date = plan.plan_end_date
        if not self.trip_purpose and hasattr(plan, "purpose"):
            self.trip_purpose = plan.purpose

    def validate_dates(self):
        if self.start_trip_date and self.end_trip_date:
            start = getdate(self.start_trip_date)
            end = getdate(self.end_trip_date)
            if start > end:
                frappe.throw("Start Trip Date cannot be after End Trip Date")

    def validate_vehicle_availability(self):
        if not self.vehicle:
            return
        conflict = frappe.db.sql("""
            SELECT name
            FROM `tabTrip Log`
            WHERE
                vehicle = %s
                AND name != %s
                AND docstatus < 2
                AND (
                    %s <= end_trip_date
                    AND %s >= start_trip_date
                )
        """, (
            self.vehicle,
            self.name or "",
            self.start_trip_date,
            self.end_trip_date
        ))
        if conflict:
            frappe.throw(
                "Vehicle is already in another trip during this time."
            )

    def validate_odometer(self):
        if self.starting_odometer and self.ending_odometer:
            if self.ending_odometer < self.starting_odometer:
                frappe.throw("Ending Odometer cannot be less than Starting Odometer")

    def on_submit(self):
        self.mark_completed()
        self.update_planning_status()
        self.update_request_status()

    def on_cancel(self):
        self.reset_planning_status()

    def mark_completed(self):
        self.trip_status = "Completed"

    def update_planning_status(self):
        frappe.db.set_value(
            "Trip Planning",
            self.trip_planning,
            "plan_status",
            "Complete"
        )

    def update_request_status(self):
        planning = frappe.get_doc("Trip Planning", self.trip_planning)
        if planning.trip_request:
            frappe.db.set_value(
                "Trip Request",
                planning.trip_request,
                "trip_request_status",
                "Completed"
            )

    def reset_planning_status(self):
        frappe.db.set_value(
            "Trip Planning",
            self.trip_planning,
            "plan_status",
            "Planned"
        )

    def calculate_distance(self):
        if self.starting_odometer and self.ending_odometer:
            distance = self.ending_odometer - self.starting_odometer
            if distance < 0:
                frappe.throw("Ending Odometer cannot be less than Starting Odometer")
            self.distance_traveled_km = distance

