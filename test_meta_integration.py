from creqit.integrations.meta import MetaIntegration

def test_meta_integration():
    # Meta entegrasyonunu başlat
    meta = MetaIntegration()
    
    # Hesap bilgilerini kontrol et
    account_info = meta.get_account_info()
    print("Hesap Bilgileri:", account_info)
    
    # Kampanyaları listele
    campaigns = meta.campaigns.get_campaigns()
    print("\nKampanyalar:")
    for campaign in campaigns:
        print(f"- {campaign['name']} (ID: {campaign['id']})")
    
    # Lead formlarını listele
    forms = meta.leads.get_lead_forms()
    print("\nLead Formları:")
    for form in forms:
        print(f"- {form['name']} (ID: {form['id']})")

if __name__ == "__main__":
    test_meta_integration() 