from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adset import AdSet

class MetaAds:
    def __init__(self, config):
        self.config = config
        self.ad_account = config.ad_account

    def create_ad(self, adset_id, creative_id, name, status='PAUSED'):
        """Yeni bir reklam oluşturur"""
        ad = self.ad_account.create_ad(
            fields=[
                'name',
                'status',
                'adset_id',
                'creative',
            ],
            params={
                'name': name,
                'adset_id': adset_id,
                'creative': {'creative_id': creative_id},
                'status': status,
            }
        )
        return ad

    def get_ads(self, fields=None):
        """Tüm reklamları listeler"""
        default_fields = [
            'name',
            'status',
            'adset_id',
            'creative',
            'insights',
        ]
        fields = fields or default_fields
        
        ads = self.ad_account.get_ads(fields=fields)
        return ads

    def get_ad(self, ad_id, fields=None):
        """Belirli bir reklamı getirir"""
        default_fields = [
            'name',
            'status',
            'adset_id',
            'creative',
            'insights',
        ]
        fields = fields or default_fields
        
        ad = Ad(ad_id)
        return ad.api_get(fields=fields)

    def update_ad(self, ad_id, **params):
        """Reklam bilgilerini günceller"""
        ad = Ad(ad_id)
        ad.update(params)
        return ad

    def delete_ad(self, ad_id):
        """Reklamı siler"""
        ad = Ad(ad_id)
        ad.delete()
        return True

    def create_creative(self, name, page_id, message, link_url, image_hash=None):
        """Yeni bir reklam kreatifi oluşturur"""
        creative = self.ad_account.create_ad_creative(
            fields=[
                'name',
                'object_story_spec',
            ],
            params={
                'name': name,
                'object_story_spec': {
                    'page_id': page_id,
                    'link_data': {
                        'message': message,
                        'link': link_url,
                        'image_hash': image_hash,
                    }
                }
            }
        )
        return creative

    def get_creatives(self, fields=None):
        """Tüm kreatifleri listeler"""
        default_fields = [
            'name',
            'object_story_spec',
            'status',
        ]
        fields = fields or default_fields
        
        creatives = self.ad_account.get_ad_creatives(fields=fields)
        return creatives 