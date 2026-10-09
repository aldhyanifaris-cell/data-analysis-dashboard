"""
Accounts Models: CustomUser, UserProfile, and UserPreferences.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(blank=True, default='', max_length=500)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    organization = models.CharField(max_length=150, blank=True, default='')
    role = models.CharField(max_length=50, default='Data Analyst')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"{self.get_full_name() or self.username} ({self.email})"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, default='')
    job_title = models.CharField(max_length=100, blank=True, default='Data Scientist')
    github_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')
    total_datasets_uploaded = models.PositiveIntegerField(default=0)
    total_analyses_run = models.PositiveIntegerField(default=0)
    total_visualizations_created = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Profile of {self.user.email}"

class UserPreferences(models.Model):
    THEME_CHOICES = [('light', 'Light'), ('dark', 'Dark'), ('system', 'System Default')]
    CHART_PALETTES = [
        ('plotly', 'Plotly Default'),
        ('seaborn', 'Seaborn Modern'),
        ('viridis', 'Viridis Gradient'),
        ('plasma', 'Plasma High-Contrast'),
        ('pastel', 'Pastel Soft')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    default_chart_palette = models.CharField(max_length=30, choices=CHART_PALETTES, default='plotly')
    email_notifications = models.BooleanField(default=True)
    auto_generate_insights = models.BooleanField(default=True)
    default_export_format = models.CharField(max_length=10, default='png')

    def __str__(self) -> str:
        return f"Preferences of {self.user.email}"
