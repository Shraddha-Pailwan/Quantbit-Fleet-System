// Copyright (c) 2026, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Expense Category Master", {
    setup: function(frm) {
        frm.fields_dict["expense_category_account"]
            .grid.get_field("account")
            .get_query = function(doc, cdt, cdn) {

                return {
                    filters: {
                        company: frm.doc.company,
                        is_group: 0
                    }
                };
            };
    },
    company: function(frm) {
        frm.clear_table("expense_category_account");
        frm.refresh_field("expense_category_account");
    }

});

