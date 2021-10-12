from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'user_status']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_status',)}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_status',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(TaskModel)
admin.site.register(APIKeyModel)
admin.site.register(RemarkModel)