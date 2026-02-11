// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Insurance Policy Register"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 0
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 0
        },
		{
            fieldname: "vehicle",
            label: "Vehicle",
            fieldtype: "Link",
            options: "Vehicle Master"
        },
        {
            fieldname: "policy_number",
            label: "Policy Number",
            fieldtype: "Data"
        }
    ]
};
