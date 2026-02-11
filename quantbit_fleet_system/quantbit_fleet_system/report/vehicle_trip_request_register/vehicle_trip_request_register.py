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
            "label": "Request ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Trip Request",
            "width": 140
        },
        {
            "label": "Company",
            "fieldname": "company",
            "fieldtype": "Link",
            "options": "Company",
            "width": 180
        },
        {
            "label": "Requested By",
            "fieldname": "requested_by",
            "fieldtype": "Link",
            "options": "Employee",
            "width": 160
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Link",
            "options": "Department",
            "width": 150
        },
        {
            "label": "Status",
            "fieldname": "trip_request_status",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": "Expected Start",
            "fieldname": "expected_trip_start_date",
            "fieldtype": "Datetime",
            "width": 160
        },
        {
            "label": "Expected End",
            "fieldname": "expected_trip_end_date",
            "fieldtype": "Datetime",
            "width": 160
        },
        {
            "label": "Purpose",
            "fieldname": "purpose",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": "Posting Date",
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120
        }
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " AND tr.posting_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND tr.posting_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    query = f"""
        SELECT
            tr.name,
            tr.company,
            tr.requested_by,
            tr.department,
            tr.trip_request_status,
            tr.expected_trip_start_date,
            tr.expected_trip_end_date,
            tr.purpose,
            tr.posting_date
        FROM
            `tabTrip Request` tr
        WHERE
            tr.docstatus < 2
            {conditions}
        ORDER BY
            tr.posting_date DESC
    """
    return frappe.db.sql(query, values, as_dict=1)
