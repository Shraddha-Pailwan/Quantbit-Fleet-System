// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt
frappe.query_reports["Vehicle Expense Register"] = {
    filters: [
        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date",
            default: frappe.datetime.month_start()
        },
        {
            fieldname: "to_date",
            label: "To Date",
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
        },
        {
            fieldname: "expense_category",
            label: "Expense Category",
            fieldtype: "Link",
            options: "Expense Category Master"
        }

    ]
};
