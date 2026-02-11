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
            "label": "Service Date",
            "fieldname": "service_date",
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
            "label": "Maintenance Type",
            "fieldname": "maintenance_type",
            "fieldtype": "Link",
            "options": "Maintenance Type Master",
            "width": 140
        },

        {
            "label": "Service Provider",
            "fieldname": "service_provider",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
        {
            "label": "Odometer",
            "fieldname": "odometer_reading",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": "Labor Charges",
            "fieldname": "labor_charges",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Parts Cost",
            "fieldname": "parts_cost",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Total Cost",
            "fieldname": "total_cost",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": "Next Service Date",
            "fieldname": "next_service_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Invoice No",
            "fieldname": "invoice_number",
            "fieldtype": "Data",
            "width": 120
        }
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " AND mr.service_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND mr.service_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    if filters.get("vehicle"):
        conditions += " AND mr.vehicle = %(vehicle)s"
        values["vehicle"] = filters.get("vehicle")

    query = f"""
        SELECT
            mr.service_date,
            mr.vehicle,
            mr.maintenance_type,
            mr.service_provider,
            mr.odometer_reading,
            mr.labor_charges,
            mr.parts_cost,
            mr.total_cost,
            mr.status,
            mr.next_service_date,
            mr.invoice_number
        FROM `tabMaintenance Record` mr
        WHERE
            mr.docstatus = 1
            {conditions}

        ORDER BY
            mr.service_date DESC

    """
    return frappe.db.sql(query, values, as_dict=1)
