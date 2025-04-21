import frappe
from frappe.model.document import Document
from creqit.meta_integration import MetaIntegration

class MetaCampaign(Document):
    def before_save(self):
        if not self.campaign_id:
            # Yeni kampanya oluştur
            meta = MetaIntegration()
            campaign = meta.create_campaign(
                name=self.campaign_name,
                objective=self.objective,
                status=self.status
            )
            self.campaign_id = campaign['id']
            
            # Bütçe ayarla
            if self.daily_budget or self.lifetime_budget:
                meta.update_campaign_budget(
                    campaign_id=self.campaign_id,
                    daily_budget=self.daily_budget,
                    lifetime_budget=self.lifetime_budget
                )
    
    def onload(self):
        if self.campaign_id:
            # Kampanya performansını güncelle
            meta = MetaIntegration()
            insights = meta.get_campaign_insights(self.campaign_id)
            if insights:
                insight = insights[0]
                self.impressions = insight.get('impressions', 0)
                self.clicks = insight.get('clicks', 0)
                self.spend = insight.get('spend', 0)
                
                # Leadleri güncelle
                self.update_leads()
    
    def update_leads(self):
        """Kampanyaya ait leadleri günceller"""
        meta = MetaIntegration()
        leads = meta.get_leads(self.campaign_id)
        
        for lead_data in leads:
            if not frappe.db.exists('Meta Lead', {'lead_id': lead_data['id']}):
                lead = frappe.get_doc({
                    'doctype': 'Meta Lead',
                    'lead_id': lead_data['id'],
                    'campaign': self.name,
                    'created_time': lead_data.get('created_time'),
                    'full_name': lead_data.get('full_name'),
                    'email': lead_data.get('email'),
                    'phone_number': lead_data.get('phone_number'),
                    'ad_name': lead_data.get('ad_name'),
                    'adset_name': lead_data.get('adset_name'),
                    'form_name': lead_data.get('form_name')
                })
                
                # Özel soruları ekle
                if lead_data.get('custom_questions'):
                    for q in lead_data['custom_questions']:
                        lead.append('custom_questions', {
                            'question': q.get('question'),
                            'answer': q.get('answer')
                        })
                
                lead.insert() 