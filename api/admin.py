from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import Patient, Doctor, MedicalHistory, AnalysisResult, Medication, Appointment
from .models import User

admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(MedicalHistory)
admin.site.register(AnalysisResult)
admin.site.register(Medication)
admin.site.register(Appointment)