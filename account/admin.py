from django.contrib import admin
from .models import Account, UserAGMInteraction

# Register your models here.

class UserAGMInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'agm', 'show_again')

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username')
admin.register(Account, AccountAdmin)
admin.register(UserAGMInteraction, UserAGMInteractionAdmin)