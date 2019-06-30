from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.models import User, Department, Position, Sextype, Statuswork
from django.contrib.auth.hashers import make_password

from django.views import View
import json, gspread, datetime
from oauth2client.service_account import ServiceAccountCredentials

@csrf_exempt
def login(request):
    if(request.method == "POST"):
        user_id = request.POST['id']
        user_pass = request.POST['password']
        print(user_id)
        # user = authenticate(request, username=user_id, password=user_pass)
        # print(user)
        # if(user == None):
        #     try:
        #         user_id = get_object_or_404(User, email=user_id).username
        #     except:
        #         return redirect(reverse('account:login'))
        user = authenticate(request, username=user_id, password=user_pass)

        if user:
            auth_login(request, user)
            if 'next' in request.POST:
                link_get_next = request.POST['next']
                print(link_get_next)
                return redirect(link_get_next)

            return redirect(reverse('account:info', args=(request.user.id,)))
        else:
            return redirect(reverse('account:login'))
        
    elif(request.method == "GET"):
        if not request.user.is_anonymous:
            return redirect(reverse('account:info', args=(request.user.id,)))

        return render(request, 'account/loginform.html')

class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, 'account/registerwithline.html')

    def post(set, request):
        email_regis = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["regis_password"]
        if (User.objects.filter(email=email_regis) or User.objects.filter(username=username)):
            text = "this email has already register"
            return JsonResponse({"Register":text}, safe=False)
        else:
            try:
                scope =  ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
                creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
                client = gspread.authorize(creds)
                sheet = client.open("employee_ref").sheet1
                data = sheet.get_all_records()
            except:
                text = "error Cant connect google sheet"
                return JsonResponse({"status":False, "message":text}, safe=False)
            
            member = 1
            found = []
            for row in data:
                if (email_regis == row['email']):
                    found.append(email_regis)
                    row['username'] = username
                    row['email'] = email_regis
                    row['password'] = password
                    insertUser(row)
                    print("register already : {}".format(email_regis))

                member+=1

            if not found:
                text = "not found email in UND data center"
                return JsonResponse({"Register":text})

            return redirect(reverse('account:login'))

def logout(request):
    auth_logout(request)
    return redirect(reverse('account:login'))

def insertUser(json_row):
    dep_id = Department.objects.get(dep_name = json_row["แผนก"])
    pos_id = Position.objects.get(pos_name = json_row["ตำแหน่ง"])
    sex_id = Sextype.objects.get(sex_type = json_row["เพศ"])
    status_worker_id = Statuswork.objects.get(status_work = json_row["สถานะปฏิบัติงาน"])
                    
    print(f"{dep_id} {pos_id} {sex_id} {status_worker_id}")

    obj = User(
            username=json_row["username"], 
            password= make_password(json_row["password"]),
            email=json_row["email"],
            nickname=json_row["ชื่อเล่น"],
            first_name=json_row["ชื่อ"],
            last_name=json_row["นามสกุล"],
            dep_name_id=dep_id.id,
            pos_name_id=pos_id.id,
            dateofbirth=datetime.datetime.strptime(json_row["วันเกิด"], "%m/%d/%Y").strftime("%Y-%m-%d"),
            dateofstart=datetime.datetime.strptime(json_row["วันเริ่มทำงาน"], "%m/%d/%Y").strftime("%Y-%m-%d"),
            phone=json_row["เบอร์โทร"],
            address=json_row["ที่อยู่"],
            sex_id=sex_id.id,
            status_work_id=status_worker_id.id
        )
    obj.save()
    
@login_required
def infomation(request,pk):
    if(request.user.id == pk):
        user_obj = User.objects.get(pk = pk)
        context = {
            "id" : user_obj.id,
            "userename" : user_obj.username,
            "name" : user_obj.fullname,
            "email" : user_obj.email
        }
        print(context)
        return render(request, 'account/infomation.html', {"context":context})

    return redirect(reverse('account:login'))
