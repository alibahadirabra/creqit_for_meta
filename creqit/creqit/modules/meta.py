import frappe

def after_install():
    """Meta entegrasyonu kurulum sonrası yapılacak işlemler"""
    create_meta_settings()
    update_doctype_modules()

def update_doctype_modules():
    """Doctype'ların modülünü Meta olarak güncelle"""
    doctypes = [
        "Meta Campaign",
        "Meta Ad Set",
        "Meta Ad",
        "Meta Lead Form",
        "Meta Lead",
        "Meta Lead Field Data",
        "Meta Settings"
    ]
    
    for doctype in doctypes:
        if frappe.db.exists("DocType", doctype):
            doc = frappe.get_doc("DocType", doctype)
            doc.module = "Meta"
            doc.save()

def create_meta_settings():
    """Meta ayarlarını oluştur"""
    if not frappe.db.exists("DocType", "Meta Settings"):
        doc = frappe.get_doc({
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
    if not frappe.db.exists("Meta Settings", "Meta Settings"):
        doc = frappe.get_doc({
            "doctype": "Meta Settings",
            "meta_settings_name": "Meta Settings",
            "auto_sync": 1,
            "sync_interval": "Daily"
        })
        doc.insert() 