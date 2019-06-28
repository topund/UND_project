from django.shortcuts import render
from django.http import JsonResponse
from managedb.models import  Department, Position, Policy, Policytype
from users.models import Profile, Remainleavedays, Suppervisor
from managedbtrans.models import History 
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime
import re

from django.core.mail import send_mail

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN_LINE)
parser = WebhookParser(settings.CHANNEL_SECRET_LINE)

def reply_message(token,message):
    line_bot_api.reply_message(
        token,
        TextSendMessage(text=message)
    )

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

@csrf_exempt
def callbackLine(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        # print(f"len events : {len(events)}")
        for event in events:
            user_line_id = event.source.user_id
            reply_token = event.reply_token

        ################################### TOP #########################################
        if((event.message.text).lower() == 'register'):
            if(Profile.objects.filter(line=user_line_id)):
                reply_message(reply_token, "register already")
            else:
                print(user_line_id)
                encr = encrypt_decrypt(user_line_id,"encrypt")
                link = f"{settings.WEB_NAME}account/signupLinePage/?token={encr}"
                reply_message(reply_token, link)
            return JsonResponse({"success" : "register success"})

        # if((event.message.text).lower() == 'register'):
        #     encr = encrypt_decrypt(user_line_id,"encrypt")
        #     # print(encr)
        #     # decr = encrypt_decrypt(encr,"decrypt")
        #     link = f"{settings.WEB_NAME}account/registerline/?token={encr}"
        #     # link = f"http://www.test.com/{encr}"
        #     reply_message(reply_token, link)

        #     # encrypt_id = "gAAAAABc96rVJZkXf5pEKmj-y0nfqPlmtqN-WMjqIKzRVytRw184NuHFd9S4MpkjYyhLx8A2p5Rl4v6uwf-dT6n_ka87rb4BAQNKMw7Js4N7TNlUp8WmT_xUtn5JXgwdrKb-eXIE1IMh"
        #     # decr = encrypt_decrypt(encrypt_id,"decrypt")
        #     # print(decr)
        #     return JsonResponse({"link" : "register success"})

        checkPro = Profile.objects.filter(line=user_line_id)
        if not (len(checkPro)>0):
            message = "no register"
            reply_message(reply_token, message)
        else:
            
            message = checkMessage(event, checkPro)

            # message = "wrong format"
            if(message != False):
                reply_message(reply_token, message)
        #############################################################################

        return JsonResponse({"call" : "POST"})
    else:
        return JsonResponse({"call" : "GET"})


def checkMessage(event, profile):
    print(event)
    profilelist = profile
    profilenow = profilelist[0]
    
    tempPo = Policytype.objects.all()
    po_list = []
    policyarr = {}
    for po in tempPo:
        policyarr[str(po)] = po.policy_key
    print(policyarr)
    # policyarr = {
    #         "ลากิจ": "personal", 
    #         "ลาพักร้อน": "vacation", 
    #         "ลาแต่งงาน": "marriage",
    #         # :"ลากิจ"
    #         }
    if(event.message.text == "คำสั่ง" or event.message.text == "word"):
        return "กาใช้งาน ผู้ใช้ user คู่มือ manual"

    elif(event.message.text == "กาใช้งาน" or
       event.message.text == "ผู้ใช้" or
       event.message.text == "user" or
       event.message.text == "คู่มือ" or
       event.message.text == "manual"
    ):
        return "ประเภทการลา วันเริ่ม วันสิ่นสุด\nลากิจ 2019/08/10 2019/08/12 คำอธิบาย"

    elif(event.message.text == "policy"
    ):
        return "ลากิจ ลาพักร้อน ลาแต่งงาน"

    else:
        result = "ไม่มีคำสั่งนี้ (Error)"
        text = event.message.text
        textArr = text.split(" ")
        if(len(textArr) != 4):
            result = False
            return result
        policyTemp = checkpolycy(policyarr, textArr[0])
        if not(policyTemp["status"]):
            result = "ประเภทการลาไม่มี"
            return result

        print(textArr)
        print(datetime.strptime(textArr[1], '%Y/%m/%d'))
        try:
            time_begin = datetime.strptime(textArr[1], '%Y/%m/%d')
            print(time_begin)
        except:
            return "เวลาเริ่มต้นผิด"
        
        try:
            time_end = datetime.strptime(textArr[2], '%Y/%m/%d')
            print(time_end)
        except:
            return "เวลาสิ้นสุดผิด"

        if((time_end - time_begin).days+1 < 1):
            return "เวลาสิ้นสุด มากกว่า เวลาเริ่มต้นผิด"
        
        jsonT = {
            "create_ad" : str(datetime.now()),
            "username": str(profilenow.user),
            "policy_type" : policyTemp["policy_key"],
            "leaveday_begin" : str(time_begin),
            "leaveday_end" : str(time_end),
            "explanation" : textArr[3]
        }
        result = insertHist(jsonT)

        return result

def checkpolycy(dictPo, text):
    for key, val in dictPo.items():
        if(key == text):
            return {"status" : True, "policy_key": val}
    return {"status" : False}


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


def insertHist(jsonreq):
    error = []
    # jsonreq = json.loads(request.body.decode("utf-8"))
        
    # jsonreq['policy_type'] =  jsonreq['policy_type'].split(" ")[0].lower()
        ####################### new ######################
    user_obj = User.objects.get(username=jsonreq['username'])
    policy_objs = Policytype.objects.filter(policy_key=jsonreq['policy_type'])[0]

    histlist = History.objects.filter(user_id = user_obj.id).filter(leaveday_begin = jsonreq["leaveday_begin"]).filter(leaveday_end = jsonreq["leaveday_end"]).filter(policy_id = policy_objs.id).filter(explanation = jsonreq["explanation"])
        # .filter(user_id = user_obj.id).filter(leaveday_begin = jsonreq["leaveday_begin"]).filter(explanation = jsonreq["explanation"]).filter(policy_id = policy_objs.id)
        # print(jsonreq["policy_type"])
    if(len(histlist) > 0):
            
        print("have hist")
        return "ทำไปแล้ว"
            
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
        return "success"
