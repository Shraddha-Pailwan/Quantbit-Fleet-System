// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Maintenance Register"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            reqd: 1
        },
        {
            fieldname: "vehicle",
            label: __("Vehicle"),
            fieldtype: "Link",
            options: "Vehicle Master"
        }
    ]
};

