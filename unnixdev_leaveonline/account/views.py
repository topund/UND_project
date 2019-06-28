from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import Profile, Remainleavedays, Suppervisor
from managedb.models import  Department, Position, Policy, Policytype, Sextype, Statuswork
from managedbtrans.models import  History
from django.contrib.auth.models import User

from django.conf import settings
from django.core import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.shortcuts import get_object_or_404

@csrf_exempt
def login(request):
    if(request.method == "POST"):
        user_id = request.POST['id']
        user_pass = request.POST['password']
        print(user_id)
        user = authenticate(request, username=user_id, password=user_pass)
        print(user)
        if(user == None):
            try:
                user_id = get_object_or_404(User, email=user_id).username
            except:
                return redirect('/user/')
        # print(test)
        user = authenticate(request, username=user_id, password=user_pass)
        # temp = User.objects.filter(password=user_pass)
        # print(dir(temp))
        
        print("s")
        print(user)
        # try:
        #     user = authenticate(request, username=user_id, password=user_pass)
        # except:
        #     user = authenticate(request, email=user_id, password=user_pass)
        if user:
            auth_login(request, user)
            return redirect('/user/')
        else:
            print("sss")
            return redirect('/user/')
            # return render(request, 'account/failform.html')
        
    elif(request.method == "GET"):
        print("loginForm")
        return render(request, 'account/loginform.html')
    
def logout(request):
    auth_logout(request)
    return redirect('/user/')

# @csrf_exempt
# def register(request):
#     if(request.method == 'POST'):
        
#         jsonreq = json.loads(request.body.decode("utf-8"))
#         print(jsonreq)
#         if (User.objects.filter(username=jsonreq["nameuser"]) or User.objects.filter(email=jsonreq["email"])):
#             return JsonResponse({"status":"error"}, safe=False)
#         else:
#             user_object = User(
#                 username=jsonreq["nameuser"], 
#                 password= make_password(jsonreq["password"]),
#                 email=jsonreq["email"],
#             )
#             user_object.save()
#             profile_object = Profile(
#                 user_id=user_object.id,
#                 dep_name_id=jsonreq["department"],
#                 pos_name_id=jsonreq["position"],
#             )
#             profile_object.save()
#             insertToRemainpol(jsonreq, user_object.id)

#             if(jsonreq["position"]  == 1 or jsonreq["position"]  == 3):
#                 supervisor = Suppervisor(
#                     dep_name_id=jsonreq["department"],
#                     sup_name_id = user_object.id,
#                 )
#                 supervisor.save()

#             return JsonResponse({"status":"finish"}, safe=False)
            
#     else:
#         dep = Department.objects.all().values('id', 'dep_name')
#         pos = Position.objects.all().values('id', 'pos_name')
#         response_data = {
#             "status": "active",
#             "position" : list(pos),
#             "department" : list(dep),
#         }
#         return JsonResponse(response_data, safe=False)

# def registerPage(request):
#     return render(request, "account/registerForm.html")

def registerLinePage(request):
    return render(request, "account/registerLineForm.html")


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
def registerLine(request):
    if(request.method == 'POST'):
        print("sss")
        jsonreq = json.loads(request.body.decode("utf-8"))
        try:
            line_id = encrypt_decrypt(jsonreq["token"], "decrypt")
            User.objects
        except:
            return JsonResponse({"status":False, "message":"error Cant decript token"}, safe=False)
        print(line_id)
        print(jsonreq)
        # print(len(Profile.objects.filter(line = line_id)))
        if len(Profile.objects.filter(line = line_id)) > 0:
            
            return JsonResponse({"status":False, "message":"error this token already register"}, safe=False)

        if (User.objects.filter(username=jsonreq["username"]) or User.objects.filter(email=jsonreq["email"])):
            return JsonResponse({"status":False}, safe=False)
        else:
            try:
                scope =  ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
                creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
                client = gspread.authorize(creds)
                sheet = client.open("employee_ref").sheet1
                data = sheet.get_all_records()
            except:
                return JsonResponse({"status":False, "message":"error Cant connect google sheet"}, safe=False)
            
            data_dump  = {}
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            for row in data:
                if (jsonreq["email"] == row['email']):
                    dep_id = Department.objects.get(dep_name = row["แผนก"])
                    pos_id = Position.objects.get(pos_name = row["ตำแหน่ง"])
                    sex_id = Sextype.objects.get(sex_type = row["เพศ"])
                    status_worker_id = Statuswork.objects.get(status_work = row["สถานะปฏิบัติงาน"])

                    data_dump = {
                        "username":jsonreq["username"],
                        "password":jsonreq["password"],
                        "email":jsonreq["email"],
                        "nickname":row["ชื่อเล่น"],
                        "firstname":row["ชื่อ"],
                        "lastname":row["นามสกุล"],
                        "department":dep_id.id,
                        "position":pos_id.id,
                        "date_birth":row["วันเกิด"],
                        "date_start":row["วันเริ่มทำงาน"],
                        "phone":row["เบอร์โทร"],
                        "address":row["ที่อยู่"],
                        "line": encrypt_decrypt(jsonreq["token"], "decrypt"),
                        "sex": sex_id.id,
                        "status_worker": status_worker_id.id
                    }
                    
                    print(data_dump)
            
            if(data_dump):
                user_object = User(
                    username=jsonreq["username"], 
                    password= make_password(jsonreq["password"]),
                    email=jsonreq["email"],
                )
                user_object.save()
                profile_object = Profile(
                    user_id=user_object.id,
                    dep_name_id=data_dump["department"],
                    pos_name_id=data_dump["position"],
                    status_work_id=data_dump["status_worker"],
                    sex_id=data_dump["sex"],
                    firstname = data_dump["firstname"],
                    lastname = data_dump["lastname"],
                    nickname = data_dump["nickname"],
                    dateofbirth = datetime.datetime.strptime(data_dump["date_birth"], "%m/%d/%Y").strftime("%Y-%m-%d"),
                    dateofstart = datetime.datetime.strptime(data_dump["date_start"], "%m/%d/%Y").strftime("%Y-%m-%d"),
                    phone = data_dump["phone"],
                    address = data_dump["address"],
                    line = data_dump['line']
                )
                profile_object.save()

                insertToRemainpol(data_dump, user_object.id)
                print(data_dump["position"])
                if("management" == str(pos_id)):
                    supervisor = Suppervisor(
                        dep_name_id = data_dump["department"],
                        sup_name_id = user_object.id,
                    )
                    supervisor.save()

                return JsonResponse({"status":True, "message": "success register"}, safe=False)

            return JsonResponse({"status":False, "message":"error no have email in google sheet"}, safe=False)

def insertToRemainpol(jsonreq, user_id):
    type_policy = list(Policytype.objects.all().values('id','policy_name','policy_key'))
    dep_id = Department.objects.get(dep_name = "all")
    pos_id = Position.objects.get(pos_name = "all")

    sex_type = Sextype.objects.get(id = jsonreq["sex"])

    print(dep_id)
    print(pos_id)
    print(user_id)
    for i in range(0,len(type_policy)):
        
        print(type_policy[i]['policy_name'])
        print(type_policy[i]['policy_key'])
        if(type_policy[i]['policy_key'] == "maternitym" and str(sex_type) == "male"):
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

