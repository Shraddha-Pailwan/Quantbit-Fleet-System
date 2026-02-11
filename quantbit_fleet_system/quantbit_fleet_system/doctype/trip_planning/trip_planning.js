// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt
frappe.ui.form.on("Trip Planning", {
    trip_request: function(frm) {
        if (!frm.doc.trip_request) return;
        fetch_from_trip_request(frm);
    },
    setup: function(frm) {
        frm.set_query("from_department", function() {
            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });
    },
    company: function(frm) {
        frm.set_value("from_department", "");
    },
    vehicle: function(frm) {
        if (!frm.doc.vehicle) return;
        fetch_driver_from_vehicle(frm);
    }
});

function fetch_from_trip_request(frm) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Trip Request",
            name: frm.doc.trip_request
        },
        callback: function(r) {
            if (!r.message) return;
            let req = r.message;
            console.log("Trip Request Data:", req);
            console.log("Department Value:", req.department);
            frm.set_value("company", req.company);
            frm.set_value("plan_start_date", req.expected_trip_start_date);
            frm.set_value("plan_end_date", req.expected_trip_end_date);
            setTimeout(() => {
                if (req.department) {
                    frm.set_value("from_department", req.department);
                }
            }, 300);
            if (req.purpose) {
                frm.set_value("purpose", req.purpose);
            }
            if (req.posting_date) {
                frm.set_value("posting_date", req.posting_date);
            }
            if (req.requested_by) {
                frm.set_value("requested_by", req.requested_by);
            }
        }
    });
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
                    title: "No Active Driver",
                    message: "No active driver assigned to this vehicle.",
                    indicator: "orange"
                });
            }
        }
    });
}
