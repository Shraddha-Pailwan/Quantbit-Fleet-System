// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Trip Request", {
    setup: function(frm) {
        frm.set_query("department", function() {
            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });
    },
    company: function(frm) {

        frm.set_value("department", "");
    }
});

