import frappe
from frappe.utils import today, add_days, getdate


def update_insurance_policy_status():

    current_date = getdate(today())

    policies = frappe.get_all(
        "Insurance Policy",
        fields=[
            "name",
            "end_date",
            "renewal_reminder_days"
        ]
    )

    for policy in policies:

        if not policy.end_date or not policy.renewal_reminder_days:
            continue

        expiry_date = getdate(policy.end_date)
        reminder_days = int(policy.renewal_reminder_days)

        due_date = add_days(expiry_date, -reminder_days)

        # FIXED LOGIC
        if current_date >= expiry_date:
            status = "Expired"

        elif current_date >= due_date:
            status = "Due"

        else:
            status = "Insured"

        frappe.db.set_value(
            "Insurance Policy",
            policy.name,
            "policy_status",
            status
        )

    frappe.db.commit()
