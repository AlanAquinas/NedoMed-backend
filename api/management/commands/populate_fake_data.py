from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import datetime, timedelta

from api.models import User, Patient, Doctor, MedicalHistory, AnalysisResult, Medication, Appointment


class Command(BaseCommand):
    help = 'Populate fake data into the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create admin user
        admin = User.objects.create_user(username='admin', email='admin@example.com', password='admin', first_name='Admin', last_name='User', user_type='admin')

        # Create patients
        for _ in range(10):
            patient = Patient.objects.create(
                user=User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password', first_name=fake.first_name(), last_name=fake.last_name(), user_type='patient'),
                date_of_birth=fake.date_of_birth(),
                blood_type=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                allergies=fake.text(),
                phone=fake.phone_number()
            )

        # Create doctors
        for _ in range(5):
            doctor = Doctor.objects.create(
                user=User.objects.create_user(username=fake.user_name(), email=fake.email(), password='password', first_name=fake.first_name(), last_name=fake.last_name(), user_type='doctor'),
                specialization=fake.job(),
                qualifications=fake.text(),
                experience_years=random.randint(1, 30),
                license_number=fake.uuid4(),
                room=random.choice(['101', '102', '103', '104', '105'])
            )

        # Create medical histories
        patients = Patient.objects.all()
        for patient in patients:
            for _ in range(3):  # Create 3 medical histories per patient
                date = fake.date_between(start_date='-1y', end_date='today')
                history = MedicalHistory.objects.create(
                    patient=patient,
                    date=date,
                    diagnosis=fake.text(),
                    prescribed_medications=fake.text(),
                    tests_conducted=fake.text()
                )

        # Create analysis results
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        for _ in range(20):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            date = fake.date_between(start_date='-1y', end_date='today')
            result = AnalysisResult.objects.create(
                patient=patient,
                doctor=doctor,
                date=date,
                conclusion=fake.text(),
                test_type=fake.word(),
                analysis_details=fake.text()
            )

        # Create medications
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        for _ in range(30):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            date_prescribed = fake.date_between(start_date='-1y', end_date='today')
            medication = Medication.objects.create(
                patient=patient,
                doctor=doctor,
                date_prescribed=date_prescribed,
                medication_name=fake.word(),
                dosage=fake.word(),
                frequency=fake.word(),
                duration_days=random.randint(1, 30)
            )

        # Create appointments
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        for _ in range(50):
            patient = random.choice(patients)
            doctor = random.choice(doctors)
            appointment_date = fake.date_between(start_date='-1y', end_date='today')
            start_time = datetime.strptime('09:00', '%H:%M') + timedelta(minutes=random.randint(0, 24) * 15)
            end_time = start_time + timedelta(minutes=15)
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                start_time=start_time.time(),
                end_time=end_time.time(),
                reason=fake.text(),
                is_accepted=random.choice([True, False]),
                notes=fake.text()
            )

        self.stdout.write(self.style.SUCCESS('Fake data inserted successfully!'))
