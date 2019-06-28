import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from .provider import CustomProvider
from django.conf import settings

class CustomAdapter(OAuth2Adapter):
    provider_id = CustomProvider.id
    # access_token_url = '{}/openid/token/'.format('http://127.0.0.1:5200')  # Called programmatically, must be reachable from container
    # authorize_url = '{}/openid/authorize/'.format('http://127.0.0.1:5200')  # This is the only URL accessed by the browser so must be reachable by the host !
    # profile_url = '{}/openid/userinfo/'.format('http://127.0.0.1:5200')

    access_token_url = '{}/openid/token/'.format(settings.UNIX_PROVIDER_URL)  # Called programmatically, must be reachable from container
    authorize_url = '{}/openid/authorize/'.format(settings.UNIX_PROVIDER_URL)  # This is the only URL accessed by the browser so must be reachable by the host !
    profile_url = '{}/openid/userinfo/'.format(settings.UNIX_PROVIDER_URL)
    
    
    def complete_login(self, request, app, token, **kwargs):
        
        # import pdb; pdb.set_trace()
        print("token : {}".format(token.token))
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(CustomAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(CustomAdapter)
