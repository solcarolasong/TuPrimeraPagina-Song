from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'user_email')
    search_fields = ('user__username', 'first_name', 'last_name', 'user__email')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    
    