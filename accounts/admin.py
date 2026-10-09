"""
Accounts Admin Configuration.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, UserPreferences

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserPreferencesInline(admin.StackedInline):
    model = UserPreferences
    can_delete = False
    verbose_name_plural = 'Preferences'

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, UserPreferencesInline)
    list_display = ('email', 'username', 'first_name', 'last_name', 'organization', 'role', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'organization')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'bio', 'avatar', 'organization', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'total_datasets_uploaded', 'total_analyses_run', 'total_visualizations_created')

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'default_chart_palette', 'email_notifications')
