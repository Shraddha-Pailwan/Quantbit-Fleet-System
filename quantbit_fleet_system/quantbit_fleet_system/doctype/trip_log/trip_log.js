frappe.ui.form.on("Trip Log", {
    trip_planning: function(frm) {
        if (!frm.doc.trip_planning) return;
        fetch_from_trip_planning(frm);
    },
    vehicle: function(frm) {
        if (!frm.doc.vehicle) return;
        fetch_driver_from_vehicle(frm);
    }
});

function fetch_from_trip_planning(frm) {
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Trip Planning",
            name: frm.doc.trip_planning
        },
        callback: function(r) {
            if (!r.message) return;
            let plan = r.message;
            frm.set_value("company", plan.company);
            frm.set_value("vehicle", plan.vehicle);
            frm.set_value("driver", plan.driver);
            frm.set_value("driver_name", plan.driver_name);
            frm.set_value("start_trip_date", plan.plan_start_date);
            frm.set_value("end_trip_date", plan.plan_end_date);
            frm.set_value("trip_request", plan.trip_request);
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
