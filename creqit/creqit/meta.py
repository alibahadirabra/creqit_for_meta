import creqit

def after_install():
    """Meta entegrasyonu kurulum sonrası yapılacak işlemler"""
    create_meta_module()
    create_meta_settings()

def create_meta_module():
    """Meta modülünü oluştur"""
    if not creqit.db.exists("Module Def", "Meta"):
        doc = creqit.get_doc({
            "doctype": "Module Def",
            "module_name": "Meta",
            "app_name": "creqit",
            "restrict_to_domain": None,
            "custom": 0,
            "color": "#FF4B4B",
            "icon": "octicon octicon-megaphone",
            "exclude_from_auto_install": 0,
            "documentation": None
        })
        doc.insert()

def create_meta_settings():
    """Meta ayarlarını oluştur"""
    if not creqit.db.exists("DocType", "Meta Settings"):
        doc = creqit.get_doc({
            "doctype": "DocType",
            "name": "Meta Settings",
            "module": "Meta",
            "custom": 0,
            "is_single": 1,
            "naming_rule": "By \"Naming Series\" field",
            "autoname": "field:meta_settings_name",
            "fields": [
                {
                    "fieldname": "meta_settings_name",
                    "fieldtype": "Data",
                    "label": "Meta Settings Name",
                    "read_only": 1,
                    "default": "Meta Settings"
                },
                {
                    "fieldname": "access_token",
                    "fieldtype": "Password",
                    "label": "Access Token"
                },
                {
                    "fieldname": "ad_account_id",
                    "fieldtype": "Data",
                    "label": "Ad Account ID"
                },
                {
                    "fieldname": "auto_sync",
                    "fieldtype": "Check",
                    "label": "Auto Sync"
                },
                {
                    "fieldname": "sync_interval",
                    "fieldtype": "Select",
                    "label": "Sync Interval",
                    "options": "Daily\nWeekly\nMonthly",
                    "default": "Daily"
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1
                }
            ]
        })
        doc.insert()

    # Meta Settings dokümanını oluştur
    if not creqit.db.exists("Meta Settings", "Meta Settings"):
        doc = creqit.get_doc({
            "doctype": "Meta Settings",
            "meta_settings_name": "Meta Settings",
            "auto_sync": 1,
            "sync_interval": "Daily"
        })
        doc.insert() 