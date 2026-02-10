# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": "Trip Date",
            "fieldname": "trip_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": "Vehicle",
            "fieldname": "vehicle",
            "fieldtype": "Link",
            "options": "Vehicle Master",
            "width": 120
        },
        {
            "label": "Driver",
            "fieldname": "driver",
            "fieldtype": "Link",
            "options": "Driver Master",
            "width": 120
        },
        {
            "label": "Driver Name",
            "fieldname": "driver_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Start Odometer",
            "fieldname": "starting_odometer",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": "End Odometer",
            "fieldname": "ending_odometer",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": "Distance (KM)",
            "fieldname": "distance_traveled_km",
            "fieldtype": "Float",
            "width": 130
        }
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " and tl.trip_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " and tl.trip_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    if filters.get("vehicle"):
        conditions += " and tl.vehicle = %(vehicle)s"
        values["vehicle"] = filters.get("vehicle")
    if filters.get("driver"):
        conditions += " and tl.driver = %(driver)s"
        values["driver"] = filters.get("driver")
    query = f"""
		SELECT
			tl.start_trip_date,
            tl.end_trip_date,
			tl.vehicle,
			tl.driver,
			dm.full_name as driver_name,
			tl.starting_odometer,
			tl.ending_odometer,
			tl.distance_traveled_km
		FROM
			`tabTrip Log` tl
		LEFT JOIN
			`tabDriver Master` dm
		ON
			tl.driver = dm.name
		WHERE
			tl.docstatus = 1   
			{conditions}
		ORDER BY
			tl.trip_date DESC
"""
    return frappe.db.sql(query, values, as_dict=1)
