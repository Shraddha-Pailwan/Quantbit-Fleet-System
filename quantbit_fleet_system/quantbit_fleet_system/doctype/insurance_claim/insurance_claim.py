# Copyright (c) 2026, Quantbit
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, nowdate

class InsuranceClaim(Document):
    def before_insert(self):
        if not self.claim_status:
            self.claim_status = "Filed"

    def validate(self):
        self.fetch_from_policy()
        self.validate_dates()
        self.validate_policy_validity()
        self.validate_amounts()
        self.validate_settlement()
        self.validate_status_flow()

    def validate_status_flow(self):
        old_status = self.get_db_value("claim_status") or "Filed"
        new_status = self.claim_status or "Filed"
        allowed_transitions = {
            "Filed": ["Under Review"],
            "Under Review": ["Approved", "Rejected"],
            "Approved": ["Settled"],
            "Rejected": [],
            "Settled": []
        }
        if old_status == new_status:
            return
        allowed = allowed_transitions.get(old_status, [])
        if new_status not in allowed:
            frappe.throw(
                f"Status cannot be changed from {old_status} to {new_status}"
            )

    def fetch_from_policy(self):
        if not self.policy:
            return
        policy = frappe.get_doc("Insurance Policy", self.policy)
        if hasattr(policy, "company") and policy.company:
            self.company = policy.company
        if hasattr(policy, "vehicle") and policy.vehicle:
            self.vehicle = policy.vehicle
            
    def validate_dates(self):
        today = getdate(nowdate())
        if self.incident_date and self.claim_date:
            incident = getdate(self.incident_date)
            claim = getdate(self.claim_date)
            if incident > claim:
                frappe.throw("Incident Date cannot be after Claim Date")
            if claim > today:
                frappe.throw("Claim Date cannot be in the future")
        if self.settlement_date and self.claim_date:
            settlement = getdate(self.settlement_date)
            claim = getdate(self.claim_date)
            if settlement < claim:
                frappe.throw("Settlement Date cannot be before Claim Date")
                
    def validate_policy_validity(self):
        if not (self.policy and self.incident_date):
            return
        policy = frappe.get_doc("Insurance Policy", self.policy)
        start = getdate(policy.start_date)
        end = getdate(policy.end_date)
        incident = getdate(self.incident_date)
        if incident < start or incident > end:
            frappe.throw(
                "Incident date is outside policy validity period"
            )

    def validate_amounts(self):
        if self.claim_amount and self.claim_amount < 0:
            frappe.throw("Claim Amount cannot be negative")
        if self.approved_amount and self.approved_amount < 0:
            frappe.throw("Approved Amount cannot be negative")
        if self.approved_amount and self.claim_amount:
            if self.approved_amount > self.claim_amount:
                frappe.throw(
                    "Approved Amount cannot be more than Claim Amount"
                )

    def validate_settlement(self):
        if self.claim_status == "Settled":
            if not self.settlement_date:
                frappe.throw("Settlement Date is mandatory for Settled claims")
            if not self.approved_amount or self.approved_amount <= 0:
                frappe.throw("Approved Amount is mandatory for Settled claims")
