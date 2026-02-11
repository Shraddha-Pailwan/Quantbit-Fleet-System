# Copyright (c) 2026, Quantbit and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from frappe.utils import getdate, today, add_days


# class VehicleDocumentDetails(Document):
#     def validate(self):
#         self.update_document_status()

#     def update_document_status(self):

#         if not self.expiry_date:
#             self.status = "Valid"
#             return
#         current_date = getdate(today())
#         expiry_date = getdate(self.expiry_date)
#         reminder_days = self.renewal_reminder_days or 0
#         reminder_days = int(reminder_days)
#         reminder_date = add_days(expiry_date, -reminder_days)
#         if current_date > expiry_date:
#             self.status = "Expired"
#         elif current_date >= reminder_date:
#             self.status = "Pending Renewal"
#         else:
#             self.status = "Valid"

