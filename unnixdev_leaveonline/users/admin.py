from django.contrib import admin
from users.models import Profile, Remainleavedays, Suppervisor

class SuppervisorAdmin(admin.ModelAdmin):
    list_display = ['dep_name', 'sup_name']
admin.site.register(Suppervisor, SuppervisorAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dep_name', 'pos_name', 'firstname', 'lastname', 'nickname', 'sex', 'dateofbirth', 'dateofstart', 'phone', 'address', 'status_work']
admin.site.register(Profile, ProfileAdmin)

class RemainleavedaysAdmin(admin.ModelAdmin):
    list_display = ['user', 'policy', 'remain_days']
admin.site.register(Remainleavedays, RemainleavedaysAdmin)