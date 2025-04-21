import creqit
from creqit.model.document import Document

class MetaDashboard(Document):
    def onload(self):
        # İstatistikleri güncelle
        self.update_stats()
    
    def update_stats(self):
        """Dashboard istatistiklerini günceller"""
        # Toplam kampanya sayısı
        self.total_campaigns = creqit.db.count('Meta Campaign')
        
        # Aktif kampanya sayısı
        self.active_campaigns = creqit.db.count('Meta Campaign', filters={'status': 'ACTIVE'})
        
        # Toplam harcama
        total_spend = creqit.db.sql("""
            SELECT SUM(spend) 
            FROM `tabMeta Campaign`
            WHERE spend IS NOT NULL
        """)[0][0] or 0
        self.total_spend = total_spend
        
        # Toplam lead sayısı
        self.total_leads = creqit.db.count('Meta Lead')
        
        # Kampanyaları getir
        campaigns = creqit.get_all('Meta Campaign', 
            fields=['name', 'campaign_name', 'status', 'impressions', 'clicks', 'spend'],
            order_by='modified DESC'
        )
        
        # Kampanya tablosunu güncelle
        self.campaigns_table = []
        for campaign in campaigns:
            self.append('campaigns_table', {
                'campaign_name': campaign.campaign_name,
                'status': campaign.status,
                'impressions': campaign.impressions,
                'clicks': campaign.clicks,
                'spend': campaign.spend
            })
        
        self.save() 