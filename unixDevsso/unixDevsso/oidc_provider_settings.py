def userinfo(claims, user):
    # Populate claims dict.
    claims['nickname'] = user.username
    claims['middle_name'] = user.first_name
    claims['family_name'] = user.last_name
    claims['email'] = user.email
    # import pdb; pdb.set_trace()

    return claims
    