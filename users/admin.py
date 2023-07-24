from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    User,
    PhoneVerificationToken,
    EmailVerificationToken
)

class NewUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'phone', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('date_joined',)}),
        ('Verification', {'fields': ('phone_verified', 'email_verified')}),
    )

    add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('email', 'password1', 'password2'),
    }),
)

admin.site.register(User, NewUserAdmin)
admin.site.register(PhoneVerificationToken)
admin.site.register(EmailVerificationToken)