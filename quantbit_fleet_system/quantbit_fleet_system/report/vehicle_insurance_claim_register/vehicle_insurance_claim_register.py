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
            "label": "Claim ID",
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Insurance Claim",
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
            "label": "Policy",
            "fieldname": "policy",
            "fieldtype": "Link",
            "options": "Insurance Policy",
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
            "label": "Driver",
            "fieldname": "driver",
            "fieldtype": "Link",
            "options": "Driver Master",
            "width": 140
        },
        {
            "label": "Driver Name",
            "fieldname": "driver_name",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": "Incident Date",
            "fieldname": "incident_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Claim Date",
            "fieldname": "claim_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": "Claim Type",
            "fieldname": "claim_type",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Claim Amount",
            "fieldname": "claim_amount",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": "Approved Amount",
            "fieldname": "approved_amount",
            "fieldtype": "Currency",
            "width": 140
        },
        {
            "label": "Status",
            "fieldname": "claim_status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Settlement Date",
            "fieldname": "settlement_date",
            "fieldtype": "Date",
            "width": 130
        }
    ]

def get_data(filters):
    conditions = ""
    values = {}
    if filters.get("from_date"):
        conditions += " AND ic.claim_date >= %(from_date)s"
        values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions += " AND ic.claim_date <= %(to_date)s"
        values["to_date"] = filters.get("to_date")
    query = f"""
        SELECT
            ic.name,
            ic.company,
            ic.policy,
            ic.vehicle,
            ic.driver,
            ic.driver_name,
            ic.incident_date,
            ic.claim_date,
            ic.claim_type,
            ic.claim_amount,
            ic.approved_amount,
            ic.claim_status,
            ic.settlement_date
        FROM
            `tabInsurance Claim` ic
        WHERE
            ic.docstatus < 2
            {conditions}

        ORDER BY
            ic.claim_date DESC
    """
    return frappe.db.sql(query, values, as_dict=1)
