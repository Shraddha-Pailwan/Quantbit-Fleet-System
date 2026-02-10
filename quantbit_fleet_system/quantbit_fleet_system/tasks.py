import frappe


def update_incomplete_plans():

    plans = frappe.get_all(
        "Trip Planning",
        filters={"plan_status": "Planned"},
        fields=["name"]
    )

    for plan in plans:

        log_exists = frappe.db.exists(
            "Trip Log",
            {"trip_planning": plan.name, "docstatus": 1}
        )

        if not log_exists:
            frappe.db.set_value(
                "Trip Planning",
                plan.name,
                "plan_status",
                "Incomplete"
            )
