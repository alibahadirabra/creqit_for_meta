from meta_integration import MetaIntegration

def main():
    # Meta entegrasyonu başlat
    meta = MetaIntegration()

    # Yeni kampanya oluştur
    new_campaign = meta.create_campaign(
        name="Test Kampanyası",
        objective="LEAD_GENERATION",
        status="PAUSED"
    )
    print("Yeni kampanya oluşturuldu:", new_campaign)

    # Tüm kampanyaları listele
    campaigns = meta.get_campaigns()
    print("\nTüm kampanyalar:")
    for campaign in campaigns:
        print(f"- {campaign['name']} (ID: {campaign['id']})")

    # Kampanya performansını görüntüle
    if campaigns:
        campaign_id = campaigns[0]['id']
        insights = meta.get_campaign_insights(campaign_id)
        print("\nKampanya performansı:")
        for insight in insights:
            print(f"Gösterim: {insight['impressions']}")
            print(f"Tıklama: {insight['clicks']}")
            print(f"Harcama: {insight['spend']}")

    # Kampanya bütçesini güncelle
    if campaigns:
        updated_campaign = meta.update_campaign_budget(
            campaign_id=campaigns[0]['id'],
            daily_budget=1000  # Günlük bütçe 10 TL
        )
        print("\nBütçe güncellendi:", updated_campaign)

if __name__ == "__main__":
    main() 