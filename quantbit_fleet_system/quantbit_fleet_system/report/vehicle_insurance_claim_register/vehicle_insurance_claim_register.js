// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Insurance Claim Register"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date"
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date"
        }
    ]
};
