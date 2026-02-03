from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, DoctorProfile, PatientProfile, Appointment

# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# -------------------------
# UserProfile Serializer
# -------------------------
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'role']


# -------------------------
# Doctor Serializer
# -------------------------
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['user', 'specialization', 'experience_years', 'available_from', 'available_to']


# -------------------------
# Appointment Serializer
# -------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'time', 'status', 'created_at']
