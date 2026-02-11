// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vehicle Master", {
    registration_number: function(frm) {
        set_vehicle_in_documents(frm);
    },
    refresh: function(frm) {
        set_vehicle_in_documents(frm);
    }
});

function set_vehicle_in_documents(frm) {
    if (!frm.doc.registration_number) return;
    if (!frm.doc.vehicle_document) return;
    frm.doc.vehicle_document.forEach(row => {
        if (!row.vehicle) {
            row.vehicle = frm.doc.registration_number;
        }
    });
    frm.refresh_field("vehicle_document");
}

