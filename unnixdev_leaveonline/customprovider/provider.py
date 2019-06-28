from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class CustomAccount(ProviderAccount):
    pass

class CustomProvider(OAuth2Provider):
    id = 'unixdev'
    name = 'Unixdev'
    account_class = CustomAccount

    def extract_uid(self, data):
        return str(data['sub'])

    def extract_common_fields(self, data):
        from pprint import pprint
        # import pdb; pdb.set_trace()
        # import pdb; pdb.set_trace()
        return dict(username=data['nickname'],
                    neam=data['nickname'],
                    email=data['email'],)
                    # first_name=data['middle_name'],
                    # last_name=data['family_name'],)

    def get_default_scope(self):
        scope = ['openid', 'profile', 'email']
        return scope

providers.registry.register(CustomProvider)