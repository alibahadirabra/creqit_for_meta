from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet

class MetaCampaigns:
    def __init__(self, config):
        self.config = config
        self.ad_account = config.ad_account

    def create_campaign(self, name, objective, status='PAUSED', daily_budget=None, lifetime_budget=None):
        """Yeni bir kampanya oluşturur"""
        params = {
            'name': name,
            'objective': objective,
            'status': status,
        }
        
        if daily_budget:
            params['daily_budget'] = daily_budget
        if lifetime_budget:
            params['lifetime_budget'] = lifetime_budget

        campaign = self.ad_account.create_campaign(
            fields=[
                'name',
                'objective',
                'status',
                'daily_budget',
                'lifetime_budget',
            ],
            params=params
        )
        return campaign

    def get_campaigns(self, fields=None):
        """Tüm kampanyaları listeler"""
        default_fields = [
            'name',
            'objective',
            'status',
            'daily_budget',
            'lifetime_budget',
            'start_time',
            'stop_time',
        ]
        fields = fields or default_fields
        
        campaigns = self.ad_account.get_campaigns(fields=fields)
        return campaigns

    def get_campaign(self, campaign_id, fields=None):
        """Belirli bir kampanyayı getirir"""
        default_fields = [
            'name',
            'objective',
            'status',
            'daily_budget',
            'lifetime_budget',
            'start_time',
            'stop_time',
        ]
        fields = fields or default_fields
        
        campaign = Campaign(campaign_id)
        return campaign.api_get(fields=fields)

    def update_campaign(self, campaign_id, **params):
        """Kampanya bilgilerini günceller"""
        campaign = Campaign(campaign_id)
        campaign.update(params)
        return campaign

    def delete_campaign(self, campaign_id):
        """Kampanyayı siler"""
        campaign = Campaign(campaign_id)
        campaign.delete()
        return True

    def get_campaign_adsets(self, campaign_id, fields=None):
        """Kampanyaya ait ad setlerini getirir"""
        default_fields = [
            'name',
            'daily_budget',
            'lifetime_budget',
            'start_time',
            'end_time',
            'targeting',
            'status',
        ]
        fields = fields or default_fields
        
        campaign = Campaign(campaign_id)
        adsets = campaign.get_ad_sets(fields=fields)
        return adsets 