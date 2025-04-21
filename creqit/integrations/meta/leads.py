from facebook_business.adobjects.lead import Lead
from facebook_business.adobjects.leadgenform import LeadgenForm

class MetaLeads:
    def __init__(self, config):
        self.config = config
        self.ad_account = config.ad_account

    def get_lead_forms(self, fields=None):
        """Tüm lead formlarını listeler"""
        default_fields = [
            'name',
            'status',
            'page_id',
            'created_time',
            'updated_time',
        ]
        fields = fields or default_fields
        
        forms = self.ad_account.get_leadgen_forms(fields=fields)
        return forms

    def get_form_leads(self, form_id, fields=None):
        """Form leadlerini getirir"""
        default_fields = [
            'created_time',
            'field_data',
            'id',
            'ad_id',
            'form_id',
            'page_id',
        ]
        fields = fields or default_fields
        
        form = LeadgenForm(form_id)
        leads = form.get_leads(fields=fields)
        return leads

    def get_lead(self, lead_id, fields=None):
        """Belirli bir lead'i getirir"""
        default_fields = [
            'created_time',
            'field_data',
            'id',
            'ad_id',
            'form_id',
            'page_id',
        ]
        fields = fields or default_fields
        
        lead = Lead(lead_id)
        return lead.api_get(fields=fields)

    def get_form_insights(self, form_id, fields=None):
        """Form performans metriklerini getirir"""
        default_fields = [
            'impressions',
            'leads',
            'cost_per_lead',
            'lead_rate',
        ]
        fields = fields or default_fields
        
        form = LeadgenForm(form_id)
        insights = form.get_insights(fields=fields)
        return insights

    def create_lead_form(self, page_id, name, questions, status='ACTIVE'):
        """Yeni bir lead formu oluşturur"""
        form = self.ad_account.create_leadgen_form(
            fields=[
                'name',
                'status',
                'questions',
            ],
            params={
                'name': name,
                'page_id': page_id,
                'questions': questions,
                'status': status,
            }
        )
        return form 