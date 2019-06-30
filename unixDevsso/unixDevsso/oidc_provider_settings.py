from django.utils.translation import ugettext as _
from oidc_provider.lib.claims import ScopeClaims

class CustomScopeClaims(ScopeClaims):
    info_profile_exten = (
        _(u'Profile_Exten'),
        _(u'Exten profile detail'),
    )

    def scope_profile_exten(self):
        dic = {
            'department': self.userinfo.get('department'),
            'position': self.userinfo.get('position'),
            'sex': self.userinfo.get('sex'),
            'address': self.userinfo.get('address'),
            'phone': self.userinfo.get('phone'),
            'status_work': self.userinfo.get('status_work'),
        }

        return dic

    # If you want to change the description of the profile scope, you can redefine it.
    info_profile_exten = (
        _(u'Profile'),
        _(u'Another description.'),
    )

def userinfo(claims, user):
    # Populate claims dict.
    # import pdb; pdb.set_trace()
    claims['nickname'] = user.username
    claims['given_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['email'] = user.email

    claims['department'] = str(user.dep_name)
    claims['position'] = str(user.pos_name)
    claims['sex'] = str(user.sex)
    claims['address'] = str(user.address)
    claims['phone'] = str(user.phone)
    claims['status_work'] = str(user.status_work)

    return claims
    