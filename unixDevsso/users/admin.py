from django.contrib import admin
from users.models import User, Department, Position, Sextype, Statuswork

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'status_work']
admin.site.register(User, UserAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'dep_name']
admin.site.register(Department, DepartmentAdmin)

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pos_name']
admin.site.register(Position, PositionAdmin)

class SextypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'sex_type']
admin.site.register(Sextype, SextypeAdmin)

class StatusworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'status_work']
admin.site.register(Statuswork, StatusworkAdmin)