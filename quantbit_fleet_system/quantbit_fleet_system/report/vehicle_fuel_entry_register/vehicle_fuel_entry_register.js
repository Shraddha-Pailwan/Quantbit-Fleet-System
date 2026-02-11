// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.query_reports["Vehicle Fuel Entry Register"] = {
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
            label: "Vehicle",
            fieldtype: "Link",
            options: "Vehicle Master"
        },
        {
            fieldname: "driver",
            label: "Driver",
            fieldtype: "Link",
            options: "Driver Master"
        }
    ]
};
