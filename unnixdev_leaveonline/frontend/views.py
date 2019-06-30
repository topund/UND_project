from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout

from django.contrib.auth.models import User


from django.http import JsonResponse

from users import models

import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

def sessionResult(request):
    json_auth = {
        "userpk": None,
        "status_login" : False,
        "user" : None,
        "email" : None,
    }
    
    try:
        if request.session.keys():
            user_id = request.session['_auth_user_id']
            user_obj = User.objects.get(pk=user_id)
            json_auth["userpk"] = user_id
            json_auth['user'] = user_obj.username
            json_auth['email'] = user_obj.email
            json_auth["status_login"] = True
            json_auth["full_name"] = '{} {}'.format(user_obj.first_name, user_obj.last_name)

            return json_auth

        else: 
            return json_auth
    except:
        return json_auth

def IndexPage(request):
    jsonSess = sessionResult(request)
    print(jsonSess)
    if(jsonSess["status_login"] == False):
        return redirect('/account/login/')
    isSuper = False
    
    temp = models.Profile.objects.filter(user = jsonSess["userpk"])
    depName = ""
    posName = ""
    for val in temp:
        depName = val.dep_name
        posName = val.pos_name
    
    if(models.Suppervisor.objects.filter(sup_name = jsonSess["userpk"]).values()):
        isSuper = True

    return render(request, 'frontend_html/index.html', {"auth_":jsonSess, "isSuper": isSuper, "depName":depName, "posName":posName})

from django.views import View
class LogOutView(View):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        
        if request.user.is_authenticated:
            logout(request)
            
        return redirect('frontend:index')


# from allauth.account.views import LoginView

# class MyLoginView(LoginView):
#     # import pdb; pdb.set_trace()
#     template_name = 'frontend_html/loginpage.html'

"http://localhost:5200/openid/authorize/?client_id=538628&redirect_uri=http%3A%2F%2Flocalhost%3A3200%2Faccount%2Funixdev%2Flogin%2Fcallback%2F&scope=email+profile+profile_exten+openid&response_type=code&state=msJoQtazMplR"