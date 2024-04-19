from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from rest_framework.permissions import IsAuthenticated


# Create your models here.

# class CustomPermissions:
#     @staticmethod
#     def create_custom_permissions():
#         # Define custom permissions for your models
#         can_view_patient_data = Permission.objects.create(
#             codename='can_view_patient_data',
#             name='Can view patient data',
#         )
#
#         can_view_doctor_data = Permission.objects.create(
#             codename='can_view_doctor_data',
#             name='Can view doctor data',
#         )
#
#         # Assign permissions to groups or users as needed
#         admin_group = Group.objects.get(name='Admin')
#         admin_group.permissions.add(can_view_patient_data, can_view_doctor_data)


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    # groups = models.ManyToManyField('auth.Group', related_name='api_user_groups', blank=True)
    # user_permissions = models.ManyToManyField('auth.Permission', related_name='api_user_permissions', blank=True)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField()
    blood_type = models.CharField(max_length=3)
    allergies = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    qualifications = models.TextField(blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    license_number = models.CharField(max_length=50, unique=True)
    room = models.CharField(max_length=5)

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField()
    diagnosis = models.TextField()
    prescribed_medications = models.TextField(blank=True, null=True)
    tests_conducted = models.TextField(blank=True, null=True)

class AnalysisResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    conclusion = models.TextField()
    test_type = models.CharField(max_length=50)
    analysis_details = models.TextField()

class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_prescribed = models.DateField()
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50, blank=True, null=True)
    duration_days = models.PositiveIntegerField(blank=True, null=True)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    reason = models.TextField()
    is_accepted = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

