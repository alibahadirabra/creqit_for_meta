app_name = "creqit"
app_title = "Creqit"
app_publisher = "Creqit"
app_description = "Creqit Application"
app_email = "support@creqit.com"
app_license = "MIT"

# Fixtures
fixtures = [
    {"doctype": "Meta Campaign", "filters": [["module", "in", ["Meta"]]]},
    {"doctype": "Meta Ad Set", "filters": [["module", "in", ["Meta"]]]},
    {"doctype": "Meta Ad", "filters": [["module", "in", ["Meta"]]]},
    {"doctype": "Meta Lead Form", "filters": [["module", "in", ["Meta"]]]},
    {"doctype": "Meta Lead", "filters": [["module", "in", ["Meta"]]]},
    {"doctype": "Meta Lead Field Data", "filters": [["module", "in", ["Meta"]]]},
    {"doctype": "Meta Lead Custom Question", "filters": [["module", "in", ["Meta"]]]}
]

# Includes
include_js = ["/assets/creqit/js/meta.js"]
include_css = ["/assets/creqit/css/meta.css"]

# DocType Class
doc_events = {
    "Meta Campaign": {
        "on_update": "creqit.integrations.meta.handlers.update_campaign",
        "on_trash": "creqit.integrations.meta.handlers.delete_campaign"
    },
    "Meta Lead Form": {
        "on_update": "creqit.integrations.meta.handlers.update_lead_form",
        "on_trash": "creqit.integrations.meta.handlers.delete_lead_form"
    }
}

# Scheduled Tasks
scheduler_events = {
    "all": [
        "creqit.integrations.meta.tasks.sync_all_campaigns"
    ],
    "daily": [
        "creqit.integrations.meta.tasks.sync_daily_insights"
    ],
    "hourly": [
        "creqit.integrations.meta.tasks.sync_hourly_leads"
    ]
} 