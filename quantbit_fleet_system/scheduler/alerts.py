import frappe
from frappe.utils import getdate, today, add_days

def daily_alerts():
    check_vehicle_documents()

def check_vehicle_documents():
    current_date = getdate(today())
    vehicles = frappe.get_all(
        "Vehicle Master",
        fields=["name", "registration_number"]
    )
    for v in vehicles:
        vehicle = frappe.get_doc("Vehicle Master", v.name)
        for doc in vehicle.vehicle_document:
            if not doc.expiry_date:
                continue
            expiry = getdate(doc.expiry_date)
            reminder_days = int(doc.renewal_reminder_days or 0)
            reminder_date = add_days(expiry, -reminder_days)
            if current_date > expiry:
                title = "Vehicle Document Expired"
                message = (
                    f"{doc.document_type} has expired for "
                    f"Vehicle {vehicle.registration_number}"
                )
                send_notification_and_email(
                    title,
                    message,
                    "Vehicle Master",
                    vehicle.name
                )
            elif current_date >= reminder_date:
                title = "Vehicle Document Renewal Due"
                message = (
                    f"{doc.document_type} needs renewal for "
                    f"Vehicle {vehicle.registration_number}"
                )
                send_notification_and_email(
                    title,
                    message,
                    "Vehicle Master",
                    vehicle.name
                )

def send_notification_and_email(title, message, ref_doctype, ref_name):
    users = frappe.get_all(
        "User",
        filters={
            "enabled": 1,
            "user_type": "System User"
        },
        fields=["name", "email"]
    )
    for user in users:
        exists = frappe.db.exists(
            "Notification Log",
            {
                "subject": title,
                "document_type": ref_doctype,
                "document_name": ref_name,
                "for_user": user.name
            }
        )
        if exists:
            continue
        frappe.get_doc({
            "doctype": "Notification Log",
            "subject": title,
            "email_content": message,
            "for_user": user.name,
            "document_type": ref_doctype,
            "document_name": ref_name,
            "type": "Alert"
        }).insert(ignore_permissions=True)
        if user.email:
            send_email_alert(
                user.email,
                title,
                message,
                ref_doctype,
                ref_name
            )
    frappe.db.commit()

def send_email_alert(to_email, subject, message, ref_doctype, ref_name):
    try:
        frappe.sendmail(
            recipients=[to_email],
            subject=subject,
            message=f"""
                <p>Hello,</p>
                <p>{message}</p>
                <p>
                    Reference:
                    {ref_doctype} - {ref_name}
                </p>
                <br>
                <p>
                    Regards,<br>
                    Fleet Management System
                </p>
            """,
            delayed=False
        )
    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Vehicle Document Email Alert Failed"
        )
