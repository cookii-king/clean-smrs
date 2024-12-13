from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'email_confirmed', 'mfa_enabled', 'created', 'updated')
    search_fields = ('username', 'email', 'name')
    list_filter = ('email_confirmed', 'mfa_enabled', 'created')
    readonly_fields = ('created', 'updated')
