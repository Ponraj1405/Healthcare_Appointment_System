from django.contrib import admin
from .models import UserProfile, DoctorProfile, PatientProfile, Appointment

admin.site.register(UserProfile)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(Appointment)
