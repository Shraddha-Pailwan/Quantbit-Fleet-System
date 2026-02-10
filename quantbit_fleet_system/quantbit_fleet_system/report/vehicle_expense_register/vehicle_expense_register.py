# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": "Posting Date",
            "fieldname": "posting_date",
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
            "label": "Expense Category",
            "fieldname": "expense_category",
            "fieldtype": "Link",
            "options": "Expense Category Master",
            "width": 150
        },
        {
            "label": "Odometer",
            "fieldname": "odometer_reading",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": "Amount",
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        }

    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " and ve.posting_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " and ve.posting_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    if filters.get("vehicle"):
        conditions += " and ve.vehicle = %(vehicle)s"
        values["vehicle"] = filters.get("vehicle")
    if filters.get("driver"):
        conditions += " and ve.driver = %(driver)s"
        values["driver"] = filters.get("driver")
    if filters.get("expense_category"):
        conditions += " and ve.expense_category = %(expense_category)s"
        values["expense_category"] = filters.get("expense_category")
    query = f"""
        SELECT
            ve.posting_date,
            ve.vehicle,
            ve.driver,
            dm.full_name AS driver_name,
            ve.expense_category,
            ve.odometer_reading,
            ve.amount
        FROM
            `tabVehicle Expense` ve
        LEFT JOIN
            `tabDriver Master` dm
        ON
            ve.driver = dm.name
        WHERE
            ve.docstatus = 1   
            {conditions}
        ORDER BY
            ve.posting_date DESC
    """
    return frappe.db.sql(query, values, as_dict=1)

