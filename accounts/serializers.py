"""
Accounts Serializers.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, UserPreferences

User = get_user_model()

class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'organization', 'role', 'avatar']
        read_only_fields = fields

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['theme', 'default_chart_palette', 'email_notifications', 'auto_generate_insights', 'default_export_format']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'job_title', 'github_url', 'linkedin_url', 'total_datasets_uploaded', 'total_analyses_run', 'total_visualizations_created']
        read_only_fields = ['total_datasets_uploaded', 'total_analyses_run', 'total_visualizations_created']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    preferences = UserPreferencesSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'avatar', 'organization', 'role', 'is_verified',
            'profile', 'preferences', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'is_verified', 'created_at', 'updated_at']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'organization', 'role', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        UserPreferences.objects.create(user=user)
        return user
