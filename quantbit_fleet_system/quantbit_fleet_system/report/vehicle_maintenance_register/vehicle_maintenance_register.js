// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Maintenance Register"] = {
    filters: [
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.month_end()
        },
        {
            fieldname: "vehicle",
            label: __("Vehicle"),
            fieldtype: "Link",
            options: "Vehicle Master"
        },
		{
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: "Scheduled\nIn Progress\nCompleted"
        }
    ]
};

