

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    
    list_display = ['email', 'username', 'account_type', 'is_email_verified', 'is_phone_verified', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_email_verified', 'is_phone_verified', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'company_name', 'phone_number']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Account Information', {
            'fields': ('account_type', 'company_name', 'company_registration', 'phone_number')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'state_province', 'postal_code', 'country')
        }),
        ('Verification', {
            'fields': ('is_email_verified', 'is_phone_verified', 'email_verification_code', 
                      'phone_verification_code', 'verification_code_created_at')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'account_type', 'phone_number')
        }),
    )