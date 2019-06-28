from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.models import User, Department, Position, Sextype, Statuswork

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

def logout(request):
    auth_logout(request)
    return redirect(reverse('account:login'))


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
