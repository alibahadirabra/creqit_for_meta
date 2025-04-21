import frappe
from frappe.model.document import Document

class MetaLead(Document):
    def before_save(self):
        if not self.lead_id:
            frappe.throw("Lead ID zorunludur")
        
        if not self.campaign:
            frappe.throw("Kampanya seçimi zorunludur")
    
    def after_insert(self):
        # Kampanyanın lead sayısını güncelle
        campaign = frappe.get_doc('Meta Campaign', self.campaign)
        campaign.save() 