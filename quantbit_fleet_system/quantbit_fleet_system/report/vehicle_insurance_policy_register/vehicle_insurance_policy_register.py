# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

# Copyright (c) 2026, Quantbit
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
            "label": "Policy Number",
            "fieldname": "policy_number",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Vehicle",
            "fieldname": "vehicle",
            "fieldtype": "Link",
            "options": "Vehicle Master",
            "width": 140
        },
        {
            "label": "Insurance Company",
            "fieldname": "insurance_company",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Policy Type",
            "fieldname": "policy_type",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Start Date",
            "fieldname": "start_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": "End Date",
            "fieldname": "end_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": "Policy Status",
            "fieldname": "policy_status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Renewal Reminder (Days)",
            "fieldname": "renewal_reminder_days",
            "fieldtype": "Int",
            "width": 160
        },
        {
            "label": "Coverage Amount",
            "fieldname": "coverage_amount",
            "fieldtype": "Currency",
            "width": 130
        }
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " AND ip.start_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND ip.end_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    query = f"""
        SELECT
            ip.policy_number,
            ip.vehicle,
            ip.insurance_company,
            ip.policy_type,
            ip.start_date,
            ip.end_date,
            ip.policy_status,
            ip.renewal_reminder_days,
            ip.coverage_amount
        FROM
            `tabInsurance Policy` ip
        WHERE
            ip.docstatus < 2
            {conditions}

        ORDER BY
            ip.end_date ASC
    """
    return frappe.db.sql(query, values, as_dict=1)
