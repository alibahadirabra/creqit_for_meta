from .campaigns import MetaCampaigns
from .ads import MetaAds
from .leads import MetaLeads
from .insights import MetaInsights
from .config import MetaConfig

class MetaIntegration:
    def __init__(self, access_token=None, ad_account_id=None):
        self.config = MetaConfig(access_token, ad_account_id)
        self.campaigns = MetaCampaigns(self.config)
        self.ads = MetaAds(self.config)
        self.leads = MetaLeads(self.config)
        self.insights = MetaInsights(self.config)

    def get_account_info(self):
        """Meta hesap bilgilerini getirir"""
        return self.config.get_account_info() 