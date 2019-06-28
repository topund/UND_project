from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.conf import settings 
import requests, datetime, pytz


@login_required
def registerLine(request):

    if(request.method == "GET"):
        
        account_social = SocialAccount.objects.get(user_id=request.user.id)
        user_token = SocialToken.objects.get(account_id=account_social.id)
        expires_token = user_token.expires_at
        time_now = pytz.utc.localize(datetime.datetime.utcnow())
        
        '''
            สามารถเอาไป ขอ refresh token ได้
        '''
        if(time_now > expires_token):
            print("token timeout : {}".format(time_now - expires_token))
            return JsonResponse({"error":"token timeout"})
            
        get_profile = requests.get("{}/openid/userinfo/?access_token={}".format(settings.UNIX_PROVIDER_URL,str(user_token)))
        body = get_profile.json()
        
        
        return JsonResponse({"REgister":"sss"})