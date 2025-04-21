import creqit
from creqit import _

def get_meta_settings():
    """Get Meta API settings from creqit"""
    return creqit.get_doc("Meta Settings")

class MetaSettings(creqit.Document):
    def validate(self):
        if not self.app_id or not self.app_secret:
            creqit.throw(_("Meta App ID and App Secret are required"))

    def get_api_credentials(self):
        return {
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "redirect_uri": self.redirect_uri or f"{creqit.utils.get_url()}/api/method/creqit.integrations.meta.oauth_callback"
        } 