from django.shortcuts import render

from django.views.generic import View

from django.http import JsonResponse

import json

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from managedb.models import Department, Position, Policy, Policytype
from managedb import models
from users.models import Profile, Remainleavedays, Suppervisor
from managedbtrans.models import History 

from django.contrib.auth.models import User
from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings

from django.db.models import Q

def send_email_leavedays(dic):
    send_mail(
        dic['title'],
        dic['message'],
        dic['emailfrom'],
        dic['emailto'],
        fail_silently=False,
    )
    print('send email success')

def date_replace(date):
    date = date.replace("T", " ")[:-1]
    return date


@csrf_exempt
def insert_history(request):
    if(request.method == "POST"):

        error = []
        jsonreq = json.loads(request.body.decode("utf-8"))
        
        jsonreq['policy_type'] =  jsonreq['policy_type'].split(" ")[0].lower()
        print(jsonreq)
        ####################### new ######################
        user_obj = User.objects.get(username=jsonreq['username'])
        policy_objs = Policytype.objects.filter(policy_key=jsonreq['policy_type'])[0]

        histlist = History.objects.filter(user_id = user_obj.id).filter(leaveday_begin = jsonreq["leaveday_begin"]).filter(leaveday_end = jsonreq["leaveday_end"]).filter(policy_id = policy_objs.id).filter(explanation = jsonreq["explanation"])
        # .filter(user_id = user_obj.id).filter(leaveday_begin = jsonreq["leaveday_begin"]).filter(explanation = jsonreq["explanation"]).filter(policy_id = policy_objs.id)
        # print(jsonreq["policy_type"])
        if(len(histlist) > 0):
            
            print("have hist")
            return JsonResponse({"status" : "have"})
            
        print("dont have hist")
        ##################################################
        # return JsonResponse({"status" : "dont have"})
        # print(jsonreq)
        user_obj = User.objects.get(username=jsonreq['username'])
        user_id = user_obj.id
        # get dep name
        profile_obj = Profile.objects.get(user_id=user_id)
        depname = profile_obj.dep_name
        supervisors_dep = Suppervisor.objects.filter(dep_name=depname)
        if(len(supervisors_dep)>0):
            sup_user_id = supervisors_dep[0].sup_name.id
        else:
            error.append(f"no one is supervisor of {depname} dep.")

        # find hr sup
        depHR = Department.objects.get(dep_name = "human resource")
        dep_HR = depHR.dep_name
        supervisors_hr = Suppervisor.objects.filter(dep_name_id=depHR.id)
        if(len(supervisors_hr)>0):
            hr_user_id = supervisors_hr[0].sup_name.id
        else:
            error.append(f"no one is supervisor of {dep_HR} dep.")
        
        # find policy_type policy_key
        policy_objs = Policytype.objects.filter(policy_key=jsonreq['policy_type'])
        if(len(policy_objs)>0):
            policy_obj = policy_objs[0]
        else:
            error.append(f"no have leave day in policy")

        # find Remain_ref 
        remain_ref_obj = Remainleavedays.objects.filter(user_id=user_id)
        if(len(remain_ref_obj)>0):
            for remain_ref in remain_ref_obj:
                if(remain_ref.policy.policy_name_id == policy_obj.id):
                    reman_ref_id = remain_ref.id
                    print(remain_ref.policy)
        else:
            error.append(f"no have leave day in remain_ref")

        if not error:
            hist_obj = History(
                user_id=user_id, 
                created_at=date_replace(jsonreq['create_ad']), 
                updated_at=date_replace(jsonreq['create_ad']), 
                leaveday_begin=date_replace(jsonreq['leaveday_begin']),
                leaveday_end=date_replace(jsonreq['leaveday_end']),
                explanation=jsonreq['explanation'],
                policy_id=policy_obj.id,
                policy_ref_id=reman_ref_id,
                user_sup_id=sup_user_id,
                sta_sup_id=3, # wait state
                user_hr_id=hr_user_id,
                sta_hr_id=3, # wait state 
                sta_user_id=3 # wait state
            )
            hist_obj.save()
            sendmailHis = hist_obj
            message = f"""
                    {sendmailHis.user} ขออนุญาต { sendmailHis.policy}
                    จาก {sendmailHis.leaveday_begin} ถึง {sendmailHis.leaveday_end}
                    link : {settings.WEB_NAME}
                    คำอธิบาย : {sendmailHis.explanation}
                """
            dic = {
                "title": f'แจ้งผลการลางาน no. {sendmailHis.id}',
                "emailfrom": settings.EMAIL_HOST_USER,
                "emailto":[sendmailHis.user_sup.email],
                'message' : message,
            }
            send_email_leavedays(dic)
            return JsonResponse({"data_hist": True}, safe=False)
        else:
            print(error)
            return JsonResponse({"error":error}, safe=False)

def update_remain(hist):
    policy_ref = hist.policy_ref_id
    user_obj = Remainleavedays.objects.get(pk=policy_ref)
    diff_days = (hist.leaveday_end - hist.leaveday_begin).days
    reamin_dif = (user_obj.remain_days-(diff_days+1))
    Remainleavedays.objects.filter(pk=policy_ref).update(remain_days=reamin_dif)

def get_policy(request):
    policys = models.Policy.objects.all()
    idpolycy = policys.values()
    keys = [k for k in policys.values()[0]][1:]
    jsonData = []
    print(policys.values()[0])
    print(keys)
    # print(policys.values()[0])
    for i in range(len(policys)):
        print(keys[0],i)
        jsonData.append([
            [keys[0], str(policys[i].policy_name), idpolycy[i][keys[0]]],
            [keys[1], str(policys[i].dep_name), idpolycy[i][keys[1]]],
            [keys[2], str(policys[i].pos_name), idpolycy[i][keys[2]]],
            [keys[3], str(policys[i].numofleave), idpolycy[i][keys[3]]], 
            ])
    # json.dumps(jsonData)
    # print(jsonData)
    return JsonResponse({"policys": jsonData})

##### SUPERVISOR MODE
@csrf_exempt
def getStaffofSupervisor(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body)
        if(jsonT["get_cover"]):
            profile = Profile.objects.get(user_id=jsonT["userpk"])
            membersofdep = Profile.objects.filter(dep_name=profile.dep_name)
            # print(membersofdep)
            mems = []
            for d in membersofdep:
                if(d.user_id == int(jsonT["userpk"])):
                    continue
                profile = Profile.objects.get(user_id=d.user_id)
                user = User.objects.get(pk=d.user_id)
                remain = Remainleavedays.objects.filter(user_id=d.user_id)
                # print(remain)
                remainT = []
                for i in remain:
                    remainT.append([str(i.policy.policy_name), i.remain_days])
                mems.append({"id": d.user_id, "username": str(user), 
                    "email": user.email, 
                    "department": str(profile.dep_name), 
                    "position": str(profile.pos_name), 
                    "remain": remainT})

            return JsonResponse({"status":True, "result": mems})
        return JsonResponse({"status":False})
    else:
        return JsonResponse({"status":False})

@csrf_exempt
def supervisorApprove(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body)
        if(jsonT["get_listApprove"]):
            # profile = Profile.objects.get(user_id=jsonT["userpk"])
            hist_list = History.objects.filter(user_sup_id = int(jsonT["userpk"])).filter(sta_sup = 3)
            keys = ["id histrory", "username", "policy", "explanation", "leaveday begin", "leaveday end"]
            result = []
            for d in hist_list:
                result.append([d.id, str(d.user), str(d.policy), str(d.explanation), str(d.leaveday_begin), str(d.leaveday_end)])

            return JsonResponse({"status":True, "results": { "keys": keys, "result": result }})

        return JsonResponse({"status":False})
    else:
        return JsonResponse({"status":False})

@csrf_exempt
def approve_reject(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body)
        status = ""
        print(jsonT)
        hist = History.objects.filter(pk = int(jsonT["id_hist"]))[0]
        sendmailHis = hist
        if(jsonT["isApprove"]):
            # print(hist.update())
            if(str(hist.user_sup.id) == str(jsonT["id_user"])):
                History.objects.filter(pk = int(jsonT["id_hist"])).update(sta_sup=1)
                # SEND EMAIL 
                message = f"""
                    {sendmailHis.user} ขออนุญาต { sendmailHis.policy}
                    จาก {sendmailHis.leaveday_begin} ถึง {sendmailHis.leaveday_end}
                    link : {settings.WEB_NAME}
                    คำอธิบาย : {sendmailHis.explanation}
                """
                dic = {
                    "title": f'แจ้งผลการลางาน no. {sendmailHis.id}',
                    "emailfrom": settings.EMAIL_HOST_USER,
                    "emailto":[sendmailHis.user_hr.email],
                    'message' : message,
                }
                send_email_leavedays(dic)

            elif(str(hist.user_hr.id) == str(jsonT["id_user"])):
                History.objects.filter(pk = int(jsonT["id_hist"])).update(sta_hr=1, sta_user=1)

                # SEND EMAIL
                message = f"""
                    {sendmailHis.user} ขออนุญาต { sendmailHis.policy}
                    จาก {sendmailHis.leaveday_begin} ถึง {sendmailHis.leaveday_end}
                    link : {settings.WEB_NAME}
                    คำอธิบาย : {sendmailHis.explanation}
                    ผลลัพธ์ ได้รับอนุญาติ
                """
                dic = {
                    "title": f'แจ้งผลการลางาน no. {sendmailHis.id}',
                    "emailfrom": settings.EMAIL_HOST_USER,
                    "emailto":[sendmailHis.user.email],
                    'message' : message,
                }
                send_email_leavedays(dic)
                update_remain(hist)

            status = "Approve Success"
        else:
            if(str(hist.user_sup.id) == str(jsonT["id_user"])):
                History.objects.filter(pk = int(jsonT["id_hist"])).update(sta_sup=2, sta_hr=2, sta_user=2)

            elif(str(hist.user_hr.id) == str(jsonT["id_user"])):
                History.objects.filter(pk = int(jsonT["id_hist"])).update(sta_hr=2, sta_user=2)

            # SEND EMAIL
            message = f"""
                    {sendmailHis.user} ขออนุญาต { sendmailHis.policy}
                    จาก {sendmailHis.leaveday_begin} ถึง {sendmailHis.leaveday_end}
                    ลิ้งค์ : {settings.WEB_NAME}
                    คำอธิบาย : {sendmailHis.explanation}
                    ผลลัพธ์ ไม่ได้รับอนุญาติ
                """
            dic = {
                    "title": f'แจ้งผลการลางาน no. {sendmailHis.id}',
                    "emailfrom": settings.EMAIL_HOST_USER,
                    "emailto":[sendmailHis.user.email],
                    'message' : message,
            }
            send_email_leavedays(dic)

            status = "Reject Success"

        return JsonResponse({"status": status})
    else:
        return JsonResponse({"status":False})
    
####### HR Mode

@csrf_exempt
def getStaffall(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body)
        if(jsonT["get_cover"]):
            profile = Profile.objects.get(user_id=jsonT["userpk"])
            membersofdep = Profile.objects.all()
            # print(membersofdep)
            mems = []
            for d in membersofdep:
                if(d.user_id == int(jsonT["userpk"])):
                    continue
                profile = Profile.objects.get(user_id=d.user_id)
                user = User.objects.get(pk=d.user_id)
                remain = Remainleavedays.objects.filter(user_id=d.user_id)
                # print(remain)ลาคลอด
                remainT = []
                for i in remain:
                    remainT.append([str(i.policy.policy_name), i.remain_days])
                mems.append({"id": d.user_id, "username": str(user), 
                    "email": user.email, 
                    "dep": str(profile.dep_name), 
                    "pos": str(profile.pos_name), 
                    "remain": remainT})

            for d in mems:
                tempCheck = False
                for remain in d["remain"]:
                    
                    if(remain[0] == "ลาคลอด"):
                        tempCheck = True 
                if not tempCheck:
                    d["remain"].append(["ลาคลอด", "ไม่มี"])
            print(mems)

            return JsonResponse({"status":True, "result": mems})
        return JsonResponse({"status":False})
    else:
        return JsonResponse({"status":False})


def checkPrega(text):
    if(text == "ลาคลอด"):
        return True
    return False

@csrf_exempt
def hrApprove(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body)
        if(jsonT["get_listApprove"]):
            
            print(jsonT)
            # profile = Profile.objects.get(user_id=jsonT["userpk"])
            hist_list = History.objects.filter(sta_sup = 1).filter(sta_hr = 3)
            print(hist_list)
            keys = ["id histrory", "username", "policy", "explanation", "leaveday begin", "leaveday end"]
            result = []
            for d in hist_list:
                result.append([d.id, str(d.user), str(d.policy), str(d.explanation), str(d.leaveday_begin), str(d.leaveday_end)])

            return JsonResponse({"status":True, "results": { "keys": keys, "result": result }})

        return JsonResponse({"status":False})
    else:
        return JsonResponse({"status":False})


@csrf_exempt
def reportFn(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body.decode("utf-8"))
        print(jsonT)
        if(jsonT['getReport']):
            profilenow = Profile.objects.get(user_id = jsonT["user_id"])
            if (str(profilenow.dep_name) == "human resource"):
                print("HR mode")
                # histlist = History.objects.all()
                user_list = User.objects.exclude(pk=1)
                
                # return 

            elif (str(profilenow.pos_name) == "management"):

                print("spervisor mode")
                # print(profilenow.dep_name)
                pro_list = Profile.objects.filter(dep_name_id = str(profilenow.dep_name_id))
                # print(test.user_id)

                # user_list = User.objects.filter(pk = jsonT["user_id"])
                user_list = []
                for pro in pro_list :
                    user_list.append(User.objects.get(pk = pro.user_id))
                
            
            elif (str(profilenow.pos_name) == "junior"):
                print("Junior mode")
                user_list = User.objects.filter(pk = jsonT["user_id"])
            
            keys = ["username", "email", "depatment", "position"]
            arr = []
            print(user_list)
            for user in user_list :
                    # if(user.pk == int(jsonT["user_id"])):
                    #     continue
                profile = Profile.objects.get(user_id = user.pk)
                arr.append([str(user.username), str(user.email), str(profile.dep_name), str(profile.pos_name)])
                    
            myself = get_reportMyself(jsonT["user_id"], profilenow)
            print("------------------------------------")
            heatgraph = get_graph_total(jsonT["user_id"])
            print(heatgraph)
            return JsonResponse({
                                "status" : True, 
                                "all" : {"keys": keys ,"data" : arr},
                                "myself" : myself,
                                "heatgraph" : heatgraph
                                })
                                
    else:
        return JsonResponse({"status" : False})

def get_reportMyself(user_id, profilenow):
    remainlist = Remainleavedays.objects.filter(user_id=user_id)
    remain_list = []
    for remain in remainlist:
        remain_list.append([str(remain.policy.policy_name), str(remain.remain_days)])
                    # remain_list.append([""])
    myself = {
        "username" : str(profilenow.user),
        "dep_name" : str(profilenow.dep_name),
        "pos_name" : str(profilenow.pos_name),
        "remain_list": remain_list,
    }
    return myself

@csrf_exempt
def get_detail(request):
    if(request.method == "POST"):
        jsonT = json.loads(request.body.decode("utf-8"))
        user = User.objects.filter(username=jsonT["username"])
        if(len(user) == 0):
            return JsonResponse({"status" : False})
        userNow = user[0]
        profilenow = Profile.objects.get(user_id = userNow.id)
        
        myself = get_reportMyself(userNow.id, profilenow)

        hist_now = get_detail_history(userNow.id)

        self_chart = get_barGraph_user(userNow.id)



        return JsonResponse({"status" : True, "myself": myself, "bar_chart": self_chart, "hist": hist_now})
    else:
        return JsonResponse({"status" : False})

def get_detail_history(user_id):
    hist_list = History.objects.filter(user_id=user_id)
    # profile = Profile.objects.get(user_id = h.user_id)
    arr = []
    keys =  ["id_hist", "username",  
            "polycy", "leave_begin", 
            "leave_end", "explanation", 
            "supervisor", "human resource", "status"]

    for h in hist_list:
        arr.append([h.pk, str(h.user), 
                str(h.policy), str(h.leaveday_begin), 
                str(h.leaveday_end), str(h.explanation),
                str(h.sta_sup), str(h.sta_hr), str(h.sta_user)
            ])

    # print(len(keys), len(arr))
    return {"keys" : keys, "data": arr}

def get_barGraph_user(user_id):
    x_legend = []
    maximum_days = []
    remain_days = []

    user_remain = Remainleavedays.objects.filter(user_id = user_id)
    # print(user_remain)
    for remain in user_remain:
        temp = {
            "policy_name": remain.policy.policy_name,
            "remain_day":  remain.remain_days
        }  

        x_legend.append(str(temp["policy_name"]))
        maximum_days.append(remain.policy.numofleave)
        remain_days.append(temp["remain_day"])

    datachart = {
        "title" : "กราฟแสดงจำนวนวันลาที่เหลือ",
        "xlegend" : x_legend,
        "ylegend" : "จำนวนของวันลา(วัน)",
        "unit": "วัน",
        "series": {
            "remain" : remain_days,
            "maximum" : maximum_days
        }
    }
    return datachart

def get_graph_total(user_id):
    import numpy as np

    print("=========================77777777777")
    user_prof = Profile.objects.filter(user_id=user_id)
    print(user_prof[0].dep_name_id)
    if(str(user_prof[0].dep_name) == "human resource"): # check HR is 4
        all_user = Profile.objects.all()
        print("=========================111111111111111")
    elif(str(user_prof[0].pos_name) == "management"):
        all_user = Profile.objects.filter(dep_name_id=user_prof[0].dep_name_id)
        print(all_user[0].user.id)
        print("=========================")
    else:
        all_user = user_prof

    policys_type = Policytype.objects.all()
    np_remain = np.zeros((len(all_user), len(policys_type)))
    np_maximum = np.zeros((len(all_user), len(policys_type)))
    user_ary = []
    leave_type_ary = [] 
    for i, user in enumerate(all_user):
        user_remains = Remainleavedays.objects.filter(user_id=user.user.id)
        for j, user_remain in enumerate(user_remains):
            for k, policy_type in enumerate(policys_type):
                if(user_remain.policy.policy_name_id == policy_type.id):
                    temp = {
                        "type": str(user_remain.policy.policy_name),
                        "user": str(user.user.username),
                        "remain":user_remain.remain_days,
                        "max" :user_remain.policy.numofleave
                    }
                    np_remain[i][j] = temp['remain']
                    np_maximum[i][j] = temp['max']

                    # leave_type_ary.append(temp['type'])

                    print(policy_type.policy_key)

        user_ary.append(temp['user'])
    leave_diff = np_maximum - np_remain # จำนวนวันที่หยุด
    reamin_diff = np_maximum - leave_diff # จำนวนวันที่เหลือ
    percen_leave = (leave_diff/np_maximum)*100 # เปอร์เซ็นที่หยุด
    dataT = np.around(percen_leave.T,2)
    dataT = np.nan_to_num(dataT)

    leave_type_ary= [str(typePol) for typePol in policys_type]

    print(leave_type_ary)
    temp_ary = []
    for j in range(0, dataT.shape[0]):
        for i in range(dataT.shape[1]-1, -1, -1):
            temp_ary.append([j,i,dataT[j][i]])
            
    datachart = {
            "title" : "กราฟแสดงจำนวนวันที่ลางาน (%)",
            "xlegend" : leave_type_ary,
            "ylegend" : user_ary,
            "unit": "%",
            "series" : {
                "name" : "เปอร์เซ็นของวันลา",
                "data" : temp_ary
            },
        }
    return datachart
    
    