import creqit
import json
import requests
from creqit import _
from creqit.utils import get_url
from creqit.config.meta import get_meta_settings

@creqit.whitelist(allow_guest=True)
def oauth_callback():
    """Handle Meta OAuth callback"""
    try:
        settings = get_meta_settings()
        code = creqit.form_dict.get('code')
        
        if not code:
            creqit.throw(_("Authorization code not received"))

        # Exchange code for access token
        token_response = requests.get(
            'https://graph.facebook.com/v19.0/oauth/access_token',
            params={
                'client_id': settings.app_id,
                'client_secret': settings.app_secret,
                'redirect_uri': settings.get_api_credentials().get('redirect_uri'),
                'code': code
            }
        )
        
        token_data = token_response.json()
        
        if 'error' in token_data:
            creqit.throw(_(token_data['error']['message']))
            
        # Store the access token securely
        settings.db_set('access_token', token_data['access_token'])
        settings.db_set('token_type', token_data['token_type'])
        
        creqit.msgprint(_("Meta integration successfully configured"))
        
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta OAuth Error"))
        creqit.throw(_("Failed to configure Meta integration: {0}").format(str(e)))

@creqit.whitelist(allow_guest=True)
def webhook():
    """Handle Meta Webhooks"""
    try:
        settings = get_meta_settings()
        
        # Verify webhook
        if creqit.request.args.get('hub.mode') == 'subscribe':
            if creqit.request.args.get('hub.verify_token') == settings.webhook_verify_token:
                return creqit.request.args.get('hub.challenge')
            return 'Invalid verify token', 403
            
        # Process webhook payload
        payload = json.loads(creqit.request.data)
        
        # Handle different webhook events
        if 'object' in payload and payload['object'] == 'page':
            for entry in payload['entry']:
                handle_page_event(entry)
                
        return 'OK'
        
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Webhook Error"))
        return 'Error', 500

def handle_page_event(entry):
    """Handle different page events from Meta"""
    try:
        if 'messaging' in entry:
            handle_messaging_event(entry['messaging'][0])
        # Add more event handlers as needed
            
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Event Handler Error"))

def handle_messaging_event(event):
    """Handle messaging events from Meta"""
    try:
        if 'message' in event:
            sender_id = event['sender']['id']
            message = event['message'].get('text', '')
            
            # Process the message as needed
            # For example, create a new document or trigger a workflow
            
    except Exception as e:
        creqit.log_error(creqit.get_traceback(), _("Meta Messaging Handler Error")) 