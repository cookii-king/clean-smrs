from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.utils.html import format_html
from django.shortcuts import redirect
from ...models import Account

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active', 'email_confirmed', 'mfa_enabled')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'email_confirmed', 'mfa_enabled')
    search_fields = ('username', 'email', 'name')
    ordering = ('email',)

    # Define readonly fields
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('email_confirmation_secret', 'mfa_secret', 'stripe_customer_id' )
        return self.readonly_fields

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'description')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created', 'deleted')}),
        ('Email Confirmation', {'fields': ('email_confirmation_secret', 'email_confirmed')}),
        ('MFA', {'fields': ('mfa_secret', 'mfa_enabled')}),
        ('Stripe', {'fields': ('stripe_customer_id',)}),
 
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2'),
        }),
    )

 
 

 

admin.site.register(Account, AccountAdmin)