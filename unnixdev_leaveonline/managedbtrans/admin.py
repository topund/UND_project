from django.contrib import admin
from managedbtrans.models import History

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'leaveday_begin','leaveday_end', 'policy', 'sta_sup', 'sta_hr', 'sta_user']
admin.site.register(History, HistoryAdmin)