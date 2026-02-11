# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    if not filters:
        filters = {}
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": "Fuel Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": "Vehicle",
            "fieldname": "vehicle",
            "fieldtype": "Link",
            "options": "Vehicle Master",
            "width": 130
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
            "label": "Fuel Type",
            "fieldname": "fuel_type",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": "Quantity (Liters)",
            "fieldname": "quantity_liters",
            "fieldtype": "Float",
            "width": 130
        },
        {
            "label": "Rate / Liter",
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": "Total Amount",
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": "Odometer Reading",
            "fieldname": "odometer_reading",
            "fieldtype": "Float",
            "width": 130
        },
        {
            "label": "Fuel Station",
            "fieldname": "fuel_station",
            "fieldtype": "Data",
            "width": 150
        }
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " AND fe.posting_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND fe.posting_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    query = f"""
        SELECT
            fe.posting_date,
            fe.vehicle,
            fe.driver,
            dm.full_name AS driver_name,
            fe.fuel_type,
            fe.quantity_liters,
            fe.rate_per_liter AS rate,
            fe.total_amount,
            fe.odometer_reading,
            fe.fuel_station
        FROM
            `tabFuel Entry` fe
        LEFT JOIN
            `tabDriver Master` dm
        ON
            fe.driver = dm.name
        WHERE
            fe.docstatus = 1
            {conditions}

        ORDER BY
            fe.posting_date DESC
    """
    return frappe.db.sql(query, values, as_dict=1)
