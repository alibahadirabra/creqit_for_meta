import frappe
from frappe.model.document import Document
from creqit.integrations.meta import MetaIntegration

class MetaCampaign(Document):
    def before_save(self):
        if not self.campaign_id:
            # Yeni kampanya oluştur
            meta = MetaIntegration()
            campaign = meta.campaigns.create_campaign(
                name=self.campaign_name,
                objective=self.objective,
                status=self.status,
                daily_budget=self.daily_budget,
                lifetime_budget=self.lifetime_budget
            )
            self.campaign_id = campaign['id']
        else:
            # Mevcut kampanyayı güncelle
            meta = MetaIntegration()
            meta.campaigns.update_campaign(
                self.campaign_id,
                name=self.campaign_name,
                status=self.status,
                daily_budget=self.daily_budget,
                lifetime_budget=self.lifetime_budget
            )

    def on_trash(self):
        if self.campaign_id:
            meta = MetaIntegration()
            meta.campaigns.delete_campaign(self.campaign_id)

    def sync_insights(self):
        """Kampanya performans metriklerini senkronize et"""
        if self.campaign_id:
            meta = MetaIntegration()
            insights = meta.insights.get_campaign_insights(self.campaign_id)
            
            if insights:
                insight = insights[0]
                self.impressions = insight.get('impressions', 0)
                self.clicks = insight.get('clicks', 0)
                self.spend = insight.get('spend', 0)
                self.reach = insight.get('reach', 0)
                self.cpm = insight.get('cpm', 0)
                self.ctr = insight.get('ctr', 0)
                
                self.save()

    def sync_adsets(self):
        """Kampanyaya ait ad setlerini senkronize et"""
        if self.campaign_id:
            meta = MetaIntegration()
            adsets = meta.campaigns.get_campaign_adsets(self.campaign_id)
            
            # Mevcut ad setlerini temizle
            self.adsets = []
            
            for adset in adsets:
                self.append('adsets', {
                    'adset_name': adset['name'],
                    'adset_id': adset['id'],
                    'status': adset['status'],
                    'daily_budget': adset.get('daily_budget', 0),
                    'lifetime_budget': adset.get('lifetime_budget', 0),
                    'start_date': adset.get('start_time'),
                    'end_date': adset.get('end_time')
                })
            
            self.save()

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