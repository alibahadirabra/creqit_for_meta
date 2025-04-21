import creqit
from creqit.model.document import Document

class MetaLead(Document):
    def before_save(self):
        if not self.lead_id:
            creqit.throw("Lead ID zorunludur")
        
        if not self.campaign:
            creqit.throw("Kampanya seçimi zorunludur")
    
    def after_insert(self):
        # Kampanyanın lead sayısını güncelle
        campaign = creqit.get_doc('Meta Campaign', self.campaign)
        campaign.save() 