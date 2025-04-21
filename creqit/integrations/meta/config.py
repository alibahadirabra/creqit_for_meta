from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
from dotenv import load_dotenv

load_dotenv()

class MetaConfig:
    def __init__(self, access_token=None, ad_account_id=None):
        self.access_token = access_token or os.getenv('META_ACCESS_TOKEN')
        self.ad_account_id = ad_account_id or os.getenv('META_AD_ACCOUNT_ID')
        self._init_api()
        self.ad_account = AdAccount(self.ad_account_id)

    def _init_api(self):
        """Facebook API'sini başlatır"""
        FacebookAdsApi.init(self.access_token)

    def get_account_info(self):
        """Meta hesap bilgilerini getirir"""
        return self.ad_account.api_get(
            fields=[
                'name',
                'account_status',
                'balance',
                'currency',
                'timezone_name',
                'business_name',
                'business_city',
                'business_country_code'
            ]
        )

    def update_access_token(self, new_token):
        """Access token'ı günceller"""
        self.access_token = new_token
        self._init_api()

    def update_ad_account(self, new_account_id):
        """Ad account ID'sini günceller"""
        self.ad_account_id = new_account_id
        self.ad_account = AdAccount(self.ad_account_id) 