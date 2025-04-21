from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from datetime import datetime, timedelta

class MetaInsights:
    def __init__(self, config):
        self.config = config
        self.ad_account = config.ad_account

    def get_campaign_insights(self, campaign_id, date_range=None, fields=None):
        """Kampanya performans metriklerini getirir"""
        default_fields = [
            'impressions',
            'clicks',
            'spend',
            'reach',
            'cpm',
            'ctr',
            'frequency',
            'unique_clicks',
            'unique_ctr',
        ]
        fields = fields or default_fields
        
        if not date_range:
            date_range = {
                'since': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'until': datetime.now().strftime('%Y-%m-%d')
            }
        
        campaign = Campaign(campaign_id)
        insights = campaign.get_insights(
            fields=fields,
            params=date_range
        )
        return insights

    def get_adset_insights(self, adset_id, date_range=None, fields=None):
        """Ad set performans metriklerini getirir"""
        default_fields = [
            'impressions',
            'clicks',
            'spend',
            'reach',
            'cpm',
            'ctr',
            'frequency',
            'unique_clicks',
            'unique_ctr',
        ]
        fields = fields or default_fields
        
        if not date_range:
            date_range = {
                'since': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'until': datetime.now().strftime('%Y-%m-%d')
            }
        
        adset = AdSet(adset_id)
        insights = adset.get_insights(
            fields=fields,
            params=date_range
        )
        return insights

    def get_ad_insights(self, ad_id, date_range=None, fields=None):
        """Reklam performans metriklerini getirir"""
        default_fields = [
            'impressions',
            'clicks',
            'spend',
            'reach',
            'cpm',
            'ctr',
            'frequency',
            'unique_clicks',
            'unique_ctr',
        ]
        fields = fields or default_fields
        
        if not date_range:
            date_range = {
                'since': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'until': datetime.now().strftime('%Y-%m-%d')
            }
        
        ad = Ad(ad_id)
        insights = ad.get_insights(
            fields=fields,
            params=date_range
        )
        return insights

    def get_account_insights(self, date_range=None, fields=None):
        """Hesap genelinde performans metriklerini getirir"""
        default_fields = [
            'impressions',
            'clicks',
            'spend',
            'reach',
            'cpm',
            'ctr',
            'frequency',
            'unique_clicks',
            'unique_ctr',
        ]
        fields = fields or default_fields
        
        if not date_range:
            date_range = {
                'since': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'until': datetime.now().strftime('%Y-%m-%d')
            }
        
        insights = self.ad_account.get_insights(
            fields=fields,
            params=date_range
        )
        return insights 