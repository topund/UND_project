from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from allauth.socialaccount.models import SocialToken, SocialAccount
from managedb.models import  Department, Position, Policy, Policytype, Sextype, Statuswork
from users.models import Profile, Remainleavedays, Suppervisor
from django.contrib.auth.models import User

from django.conf import settings 
import requests, datetime, pytz
import json

def encrypt_decrypt(id_line, mode):
    from cryptography.fernet import Fernet
    # key = Fernet.generate_key()  
    f = Fernet(settings.FERNET_KEY.encode())
    if(mode == "encrypt"):
        id_line_en = id_line.encode()
        encrypted = f.encrypt(id_line_en)
        return encrypted.decode()

    elif(mode == "decrypt"):
        id_line_en = id_line.encode()
        return f.decrypt(id_line_en).decode()

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
        # User.objects.filter(pk=request.user.id).update(first_name=body['given_name'], last_name=body['family_name'])


        dep = Department.objects.filter(dep_name=body["department"])
        body["department"] = dep[0].id
        pos = Position.objects.filter(pos_name=body["position"])
        body["position"] = pos[0].id
        body["position_name"] = str(pos[0]) 
        sex = Sextype.objects.filter(sex_type=body["sex"])
        body["sex"] = sex[0].id
        body["line"] = encrypt_decrypt(request.GET['token'], "decrypt")
        
        profile_obj = Profile.objects.filter(user_id=request.user.id)
        if not profile_obj:
            print("-----------------------------------------")
            print("------------ don't register -------------")
            print("-----------------------------------------")
            insertProfile(body, request.user.id)
            insertToRemainpol(body, request.user.id)
        else:
            # update id line
            print("-----------------------------------------")
            print("------------ update line ----------------")
            print("-----------------------------------------")
            profile_obj.update(line=body["line"])
        
        return redirect(reverse('frontend:index'))

def insertProfile(body, user_id):
    proobj =  Profile(
                    user_id=user_id,
                    dep_name_id=body["department"],
                    pos_name_id=body["position"],
                    status_work_id=1,
                    sex_id=body["sex"],
                    firstname = body['given_name'],
                    lastname = body['family_name'],
                    nickname = body["nickname"],
                    dateofbirth = datetime.datetime.now(),
                    dateofstart = datetime.datetime.now(),
                    phone = body["phone"],
                    address = "Address null",
                    line = body["line"]
                )
        
    proobj.save()
    if("management" == body["position_name"]):
        supervisor = Suppervisor(
            dep_name_id = body["department"],
            sup_name_id = user_id,
        )
        supervisor.save()

def insertToRemainpol(jsonreq, user_id):
    type_policy = list(Policytype.objects.all().values('id','policy_name','policy_key'))
    dep_id = Department.objects.get(dep_name = "all")
    pos_id = Position.objects.get(pos_name = "all")

    sex_type = Sextype.objects.get(id = jsonreq["sex"])
    print(sex_type)
    print(dep_id)
    print(pos_id)
    print(user_id)

    for i in range(0,len(type_policy)):

        print(type_policy[i]['policy_name'])
        print(type_policy[i]['policy_key'])
        if(type_policy[i]['policy_key'] == "maternity" and str(sex_type) == "male"):
            print("male")
            continue

        check2All = Policy.objects.filter(policy_name_id=type_policy[i]['id'],dep_name_id=dep_id.id,pos_name_id=pos_id.id)
        if(check2All):
            print("Dep | all Pos | all")
            policy_obj = check2All[0]
        else:
            checkDepAll = Policy.objects.filter(policy_name_id=type_policy[i]['id'],dep_name_id=dep_id.id,pos_name_id=jsonreq['position'])
            if(checkDepAll):
                policy_obj = checkDepAll[0]
                print(f"Dep | all Pos | {jsonreq['position']}")
            else:
                checCustom = Policy.objects.filter(policy_name_id=type_policy[i]['id'], dep_name_id=jsonreq['department'], pos_name_id=jsonreq['position'])
                policy_obj = checCustom[0]

        remain_object = Remainleavedays(
            user_id=user_id,
            policy_id=policy_obj.id,
            remain_days=policy_obj.numofleave,
        )
        remain_object.save()

