import frappe
from frappe.model.document import Document
from creqit.integrations.meta import MetaIntegration

class MetaLeadForm(Document):
    def before_save(self):
        if not self.form_id:
            # Yeni lead formu oluştur
            meta = MetaIntegration()
            form = meta.leads.create_lead_form(
                page_id=self.page_id,
                name=self.form_name,
                questions=self.get_questions_data(),
                status=self.status
            )
            self.form_id = form['id']
        else:
            # Mevcut formu güncelle
            meta = MetaIntegration()
            # Not: Meta API'si form güncelleme işlemini desteklemiyor
            pass

    def on_trash(self):
        if self.form_id:
            meta = MetaIntegration()
            # Not: Meta API'si form silme işlemini desteklemiyor
            pass

    def sync_insights(self):
        """Form performans metriklerini senkronize et"""
        if self.form_id:
            meta = MetaIntegration()
            insights = meta.leads.get_form_insights(self.form_id)
            
            if insights:
                insight = insights[0]
                self.impressions = insight.get('impressions', 0)
                self.leads = insight.get('leads', 0)
                self.cost_per_lead = insight.get('cost_per_lead', 0)
                self.lead_rate = insight.get('lead_rate', 0)
                
                self.save()

    def sync_leads(self):
        """Form leadlerini senkronize et"""
        if self.form_id:
            meta = MetaIntegration()
            leads = meta.leads.get_form_leads(self.form_id)
            
            # Mevcut leadleri temizle
            self.leads_table = []
            
            for lead in leads:
                lead_doc = frappe.get_doc({
                    'doctype': 'Meta Lead',
                    'lead_id': lead['id'],
                    'form': self.name,
                    'created_date': lead['created_time'],
                    'ad_id': lead.get('ad_id'),
                    'page_id': lead.get('page_id')
                })
                
                # Field data'yı ekle
                for field in lead.get('field_data', []):
                    lead_doc.append('field_data', {
                        'field_name': field.get('name'),
                        'field_value': field.get('values', [])[0] if field.get('values') else ''
                    })
                
                lead_doc.insert()
                self.append('leads_table', {
                    'lead': lead_doc.name
                })
            
            self.save()

    def get_questions_data(self):
        """Form sorularını Meta API formatına dönüştür"""
        questions = []
        for question in self.questions:
            questions.append({
                'type': question.type,
                'label': question.label,
                'required': question.required
            })
        return questions 