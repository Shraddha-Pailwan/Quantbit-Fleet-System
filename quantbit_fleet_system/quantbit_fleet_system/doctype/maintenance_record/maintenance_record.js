// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Maintenance Record", {
    labor_charges: function(frm) {
        calculate_total(frm);
    },
    parts_cost: function(frm) {
        calculate_total(frm);
    }
});

function calculate_total(frm) {
    let labor = frm.doc.labor_charges || 0;
    let parts = frm.doc.parts_cost || 0;
    let total = labor + parts;
    frm.set_value("total_cost", total);
}

