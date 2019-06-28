from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # path('', views.index, name='index'),

    # path('signup/', views.register, name='signup'),
    # path('signupPage/', views.registerPage, name="signuppage"),

    path('signin/', views.login, name='signin'),
    path('signout/', views.logout, name='signout'),

    path('signupLinePage/', views.registerLinePage, name="signuplinepage"),
    path('signupLine/', views.registerLine, name="signupLine")
]