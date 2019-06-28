from django.urls import path

from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.IndexPage, name='index'),
    
    path('accounts/logout', views.LogOutView.as_view(), name='logout')


]