from django.urls import path

from . import views

app_name = 'apiLeave'

urlpatterns = [
    # path('readsheetgoogle', views.ReadFromSheet.as_view(), name='readsheetgoogle'),
    path('get_policys', views.get_policy, name="policys"),


    path('insertHist', views.insert_history, name="insertHist"),

    # sipervisor link

    path('get_coverofsuper', views.getStaffofSupervisor, name="coverofsuper"),
    path('suppervisorApprove', views.supervisorApprove, name="supapprove"),
    path('approve_reject', views.approve_reject, name="approve_reject"),

    # HR link

    path('get_coverall', views.getStaffall, name="coverall"),
    path('hrApprove', views.hrApprove, name="hrapprove"),

    # Report part
    path('report', views.reportFn, name="report"),
    path('get_detail', views.get_detail, name="detail"),

]