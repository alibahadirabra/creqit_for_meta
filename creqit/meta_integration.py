from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.lead import Lead
import os
from dotenv import load_dotenv

load_dotenv()

class MetaIntegration:
    def __init__(self, access_token=None, ad_account_id=None):
        self.access_token = access_token or os.getenv('META_ACCESS_TOKEN')
        self.ad_account_id = ad_account_id or os.getenv('META_AD_ACCOUNT_ID')
        FacebookAdsApi.init(self.access_token)
        self.ad_account = AdAccount(self.ad_account_id)

    def create_campaign(self, name, objective, status='PAUSED'):
        """Yeni bir kampanya oluşturur"""
        campaign = self.ad_account.create_campaign(
            fields=[
                'name',
                'objective',
                'status',
            ],
            params={
                'name': name,
                'objective': objective,
                'status': status,
            }
        )
        return campaign

    def get_campaigns(self):
        """Tüm kampanyaları listeler"""
        campaigns = self.ad_account.get_campaigns(
            fields=[
                'name',
                'objective',
                'status',
                'daily_budget',
                'lifetime_budget',
            ]
        )
        return campaigns

    def get_campaign_insights(self, campaign_id):
        """Kampanya performans metriklerini getirir"""
        campaign = Campaign(campaign_id)
        insights = campaign.get_insights(
            fields=[
                'impressions',
                'clicks',
                'spend',
                'reach',
                'cpm',
                'ctr',
            ]
        )
        return insights

    def get_leads(self, form_id):
        """Form leadlerini getirir"""
        leads = Lead(form_id).get_leads()
        return leads

    def get_campaign_budget(self, campaign_id):
        """Kampanya bütçesini getirir"""
        campaign = Campaign(campaign_id)
        budget = campaign.api_get(
            fields=[
                'daily_budget',
                'lifetime_budget',
                'spend_cap',
            ]
        )
        return budget

    def update_campaign_budget(self, campaign_id, daily_budget=None, lifetime_budget=None):
        """Kampanya bütçesini günceller"""
        campaign = Campaign(campaign_id)
        params = {}
        if daily_budget:
            params['daily_budget'] = daily_budget
        if lifetime_budget:
            params['lifetime_budget'] = lifetime_budget
        
        campaign.update(params)
        return campaign 