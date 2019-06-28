from django.urls import path

from . import views

urlpatterns = [
    path('callbackline', views.callbackLine, name='callbackline'),
]