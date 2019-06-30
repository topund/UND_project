from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('registerLine/', views.registerLine , name='registerLine'),
    path('bypass/', views.bypass , name='bypass'),
]