import creqit
import requests
import json
from creqit import _
from creqit.utils import get_url
from creqit.config.meta import get_meta_settings

class MetaAdsAPI:
    def __init__(self):
        self.settings = get_meta_settings()
        self.base_url = "https://graph.facebook.com/v19.0"
        self.access_token = self.settings.get_password('access_token')
        
    def _make_request(self, method, endpoint, params=None, data=None):
        """Make API request to Meta Ads API"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            creqit.log_error(creqit.get_traceback(), _("Meta Ads API Error"))
            creqit.throw(_("Meta Ads API Error: {0}").format(str(e)))

    def get_ad_accounts(self):
        """Get list of ad accounts"""
        endpoint = "me/adaccounts"
        params = {
            "fields": "id,name,account_status,currency,timezone_name"
        }
        return self._make_request("GET", endpoint, params)

    def get_campaigns(self, ad_account_id):
        """Get campaigns for an ad account"""
        endpoint = f"{ad_account_id}/campaigns"
        params = {
            "fields": "id,name,status,objective,daily_budget,lifetime_budget,start_time,stop_time"
        }
        return self._make_request("GET", endpoint, params)

    def create_campaign(self, ad_account_id, campaign_data):
        """Create a new campaign"""
        endpoint = f"{ad_account_id}/campaigns"
        return self._make_request("POST", endpoint, data=campaign_data)

    def update_campaign(self, campaign_id, campaign_data):
        """Update an existing campaign"""
        endpoint = f"{campaign_id}"
        return self._make_request("POST", endpoint, data=campaign_data)

    def get_campaign_insights(self, campaign_id, date_preset="last_30d"):
        """Get campaign performance insights"""
        endpoint = f"{campaign_id}/insights"
        params = {
            "date_preset": date_preset,
            "fields": "impressions,clicks,spend,cpm,cpc,ctr"
        }
        return self._make_request("GET", endpoint, params)

    def get_ad_sets(self, campaign_id):
        """Get ad sets for a campaign"""
        endpoint = f"{campaign_id}/adsets"
        params = {
            "fields": "id,name,status,daily_budget,lifetime_budget,start_time,stop_time,targeting"
        }
        return self._make_request("GET", endpoint, params)

    def create_ad_set(self, campaign_id, ad_set_data):
        """Create a new ad set"""
        endpoint = f"{campaign_id}/adsets"
        return self._make_request("POST", endpoint, data=ad_set_data)

    def get_ads(self, ad_set_id):
        """Get ads for an ad set"""
        endpoint = f"{ad_set_id}/ads"
        params = {
            "fields": "id,name,status,creative"
        }
        return self._make_request("GET", endpoint, params)

    def create_ad(self, ad_set_id, ad_data):
        """Create a new ad"""
        endpoint = f"{ad_set_id}/ads"
        return self._make_request("POST", endpoint, data=ad_data)

    def create_ad_creative(self, ad_account_id, creative_data):
        """Create a new ad creative"""
        endpoint = f"{ad_account_id}/adcreatives"
        return self._make_request("POST", endpoint, data=creative_data)

    def create_lead_form(self, page_id, form_data):
        """Create a new lead form"""
        endpoint = f"{page_id}/leadgen_forms"
        return self._make_request("POST", endpoint, data=form_data)

    def get_lead_forms(self, page_id):
        """Get lead forms for a page"""
        endpoint = f"{page_id}/leadgen_forms"
        params = {
            "fields": "id,name,status,page_id,created_time,updated_time"
        }
        return self._make_request("GET", endpoint, params)

    def get_lead_form_leads(self, form_id):
        """Get leads from a lead form"""
        endpoint = f"{form_id}/leads"
        params = {
            "fields": "id,created_time,field_data"
        }
        return self._make_request("GET", endpoint, params)

    def create_ab_test(self, ad_account_id, test_data):
        """Create an A/B test"""
        endpoint = f"{ad_account_id}/adstudies"
        return self._make_request("POST", endpoint, data=test_data)

    def get_ab_test_results(self, test_id):
        """Get A/B test results"""
        endpoint = f"{test_id}"
        params = {
            "fields": "id,name,status,objectives,results"
        }
        return self._make_request("GET", endpoint, params)

    def create_instagram_ad(self, ad_set_id, ad_data):
        """Create an Instagram ad"""
        endpoint = f"{ad_set_id}/ads"
        ad_data["platform"] = "instagram"
        return self._make_request("POST", endpoint, data=ad_data)

    def get_instagram_insights(self, ad_id):
        """Get Instagram ad insights"""
        endpoint = f"{ad_id}/insights"
        params = {
            "fields": "impressions,reach,engagement,clicks,spend"
        }
        return self._make_request("GET", endpoint, params)

@creqit.whitelist()
def sync_campaigns(ad_account_id):
    """Sync campaigns from Meta to creqit"""
    try:
        api = MetaAdsAPI()
        campaigns = api.get_campaigns(ad_account_id)
        
        for campaign in campaigns.get('data', []):
            # Check if campaign exists
            existing_campaign = creqit.get_all(
                "Meta Campaign",
                filters={"campaign_id": campaign['id']},
                limit=1
            )
            
            if existing_campaign:
                doc = creqit.get_doc("Meta Campaign", existing_campaign[0].name)
            else:
                doc = creqit.new_doc("Meta Campaign")
            
            # Update campaign data
            doc.update({
                "campaign_name": campaign.get('name'),
                "campaign_id": campaign.get('id'),
                "status": campaign.get('status'),
                "objective": campaign.get('objective'),
                "daily_budget": campaign.get('daily_budget'),
                "lifetime_budget": campaign.get('lifetime_budget'),
                "start_time": campaign.get('start_time'),
                "stop_time": campaign.get('stop_time'),
                "ad_account_id": ad_account_id
            })
            
            # Get and update performance metrics
            insights = api.get_campaign_insights(campaign['id'])
            if insights.get('data'):
                metrics = insights['data'][0]
                doc.update({
                    "impressions": metrics.get('impressions', 0),
                    "clicks": metrics.get('clicks', 0),
                    "spend": metrics.get('spend', 0),
                    "cpm": metrics.get('cpm', 0),
                    "cpc": metrics.get('cpc', 0),
                    "ctr": metrics.get('ctr', 0)
                })
            
            doc.save()
            
        creqit.msgprint(_("Campaigns synced successfully"))
        
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Campaign Sync Error"))
        creqit.throw(_("Failed to sync campaigns: {0}").format(str(e)))

@creqit.whitelist()
def create_campaign(ad_account_id, campaign_data):
    """Create a new campaign in Meta"""
    try:
        api = MetaAdsAPI()
        response = api.create_campaign(ad_account_id, campaign_data)
        
        if 'id' in response:
            # Create campaign in creqit
            doc = creqit.new_doc("Meta Campaign")
            doc.update({
                "campaign_name": campaign_data.get('name'),
                "campaign_id": response['id'],
                "status": campaign_data.get('status', 'ACTIVE'),
                "objective": campaign_data.get('objective'),
                "daily_budget": campaign_data.get('daily_budget'),
                "lifetime_budget": campaign_data.get('lifetime_budget'),
                "start_time": campaign_data.get('start_time'),
                "stop_time": campaign_data.get('stop_time'),
                "ad_account_id": ad_account_id
            })
            doc.insert()
            
            creqit.msgprint(_("Campaign created successfully"))
            return doc.name
            
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Campaign Creation Error"))
        creqit.throw(_("Failed to create campaign: {0}").format(str(e)))

@creqit.whitelist()
def create_lead_form(page_id, form_data):
    """Create a new lead form"""
    try:
        api = MetaAdsAPI()
        response = api.create_lead_form(page_id, form_data)
        
        if 'id' in response:
            creqit.msgprint(_("Lead form created successfully"))
            return response['id']
            
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Lead Form Creation Error"))
        creqit.throw(_("Failed to create lead form: {0}").format(str(e)))

@creqit.whitelist()
def sync_lead_forms(page_id):
    """Sync lead forms from Meta"""
    try:
        api = MetaAdsAPI()
        forms = api.get_lead_forms(page_id)
        
        for form in forms.get('data', []):
            # Store lead form data in creqit
            # You can create a new DocType for lead forms if needed
            
        creqit.msgprint(_("Lead forms synced successfully"))
        
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Lead Form Sync Error"))
        creqit.throw(_("Failed to sync lead forms: {0}").format(str(e)))

@creqit.whitelist()
def create_ab_test(ad_account_id, test_data):
    """Create an A/B test"""
    try:
        api = MetaAdsAPI()
        response = api.create_ab_test(ad_account_id, test_data)
        
        if 'id' in response:
            creqit.msgprint(_("A/B test created successfully"))
            return response['id']
            
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta A/B Test Creation Error"))
        creqit.throw(_("Failed to create A/B test: {0}").format(str(e)))

@creqit.whitelist()
def create_instagram_ad(ad_set_id, ad_data):
    """Create an Instagram ad"""
    try:
        api = MetaAdsAPI()
        response = api.create_instagram_ad(ad_set_id, ad_data)
        
        if 'id' in response:
            creqit.msgprint(_("Instagram ad created successfully"))
            return response['id']
            
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Instagram Ad Creation Error"))
        creqit.throw(_("Failed to create Instagram ad: {0}").format(str(e)))

@creqit.whitelist()
def generate_report(ad_account_id, report_type, date_range):
    """Generate a custom report"""
    try:
        api = MetaAdsAPI()
        endpoint = f"{ad_account_id}/insights"
        
        params = {
            "date_preset": date_range,
            "fields": "impressions,reach,clicks,spend,cpm,cpc,ctr"
        }
        
        if report_type == "campaign":
            params["level"] = "campaign"
        elif report_type == "adset":
            params["level"] = "adset"
        elif report_type == "ad":
            params["level"] = "ad"
            
        response = api._make_request("GET", endpoint, params)
        
        # Process and format the report data
        report_data = []
        for item in response.get('data', []):
            report_data.append({
                "id": item.get('id'),
                "name": item.get('name'),
                "impressions": item.get('impressions', 0),
                "reach": item.get('reach', 0),
                "clicks": item.get('clicks', 0),
                "spend": item.get('spend', 0),
                "cpm": item.get('cpm', 0),
                "cpc": item.get('cpc', 0),
                "ctr": item.get('ctr', 0)
            })
            
        return report_data
        
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Report Generation Error"))
        creqit.throw(_("Failed to generate report: {0}").format(str(e))) 