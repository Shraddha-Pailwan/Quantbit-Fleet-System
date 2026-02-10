// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Fuel Entry", {
    vehicle: function(frm) {
        if (!frm.doc.vehicle) return;
        fetch_driver_from_vehicle(frm);
    },
    quantity_liters: function(frm) {
        calculate_total(frm);
    },
    rate_per_liter: function(frm) {
        calculate_total(frm);
    }
});

function calculate_total(frm) {
    let qty = frm.doc.quantity_liters || 0;
    let rate = frm.doc.rate_per_liter || 0;
    let total = qty * rate;
    frm.set_value("total_amount", total);
}

function fetch_driver_from_vehicle(frm) {
    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Vehicle Assignment",
            filters: {
                vehicle: frm.doc.vehicle,
                status: "Active",
                docstatus: ["<", 2]
            },
            fields: ["driver", "modified"],
            order_by: "modified desc",
            limit_page_length: 1
        },
        callback: function(r) {
            if (r.message && r.message.length > 0) {
                let assignment = r.message[0];
                frm.set_value("driver", assignment.driver);
            } else {
                frm.set_value("driver", "");
                frappe.msgprint({
                    title: "No Driver Found",
                    message: "No active driver assigned to this vehicle.",
                    indicator: "orange"
                });
            }
        }
    });
}
