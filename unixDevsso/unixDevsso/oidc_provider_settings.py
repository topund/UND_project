from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims

class CustomScopeClaims(ScopeClaims):

    info_profile_exten = (
        _(u'Profile_Exten'),
        _(u'Exten profile detail'),
    )

    def scope_profile_exten(self):
        dic = {
            'bar': 'Something dynamic here',
        }

        return dic

    # If you want to change the description of the profile scope, you can redefine it.
    info_profile = (
        _(u'Profile'),
        _(u'Another description.'),
    )

def userinfo(claims, user):
    # Populate claims dict.
    claims['nickname'] = user.username
    claims['middle_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['email'] = user.email

    return claims
    