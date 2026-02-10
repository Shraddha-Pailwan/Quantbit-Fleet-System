// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Insurance Claim", {
    vehicle: function(frm) {
        if (!frm.doc.vehicle) return;
        fetch_driver_from_vehicle(frm);
    }
});

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
                frappe.msgprint({
                    title: "No Active Driver",
                    message: "No active driver assigned to this vehicle.",
                    indicator: "orange"
                });
                frm.set_value("driver", "");
            }
        }
    });
}

frappe.ui.form.on("Insurance Claim", {
    policy: function(frm) {
        if (!frm.doc.policy) return;
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Insurance Policy",
                name: frm.doc.policy
            },
            callback: function(r) {
                if (!r.message) return;
                let policy = r.message;
                frm.set_value("company", policy.company);
                frm.set_value("vehicle", policy.vehicle);
            }
        });
    }
});
