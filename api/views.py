from rest_framework.decorators import api_view
from rest_framework_simplejwt.settings import api_settings

from .models import Patient, Doctor, Appointment, User, AppointmentListSerializer, Medication, AnalysisResult
from .serializers import (
    UserSerializer, PatientSerializer, DoctorSerializer, AppointmentSerializer, AppointmentCreateSerializer,
    AppointmentDetailSerializer, MedicationSerializer, AnalysisResultSerializer
)
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    print(username, password)
    print(User.objects)
    user = User.objects.get(username=username, password=password)
    if user is not None:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'token': token}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientDataView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class DoctorDataView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class AllDoctorsDataView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class UserMedicationsByIDView(generics.ListAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        return Medication.objects.filter(patient__user=user)

class UserAnalysisResultsByIDView(generics.ListAPIView):
    serializer_class = AnalysisResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        user = get_object_or_404(User, id=user_id)
        return AnalysisResult.objects.filter(patient__user=user)

class UserAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve appointments for the authenticated user
        user = self.request.user
        return Appointment.objects.filter(patient__user=user)

class AppointmentDetailView(generics.RetrieveAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentDetailSerializer
    lookup_field = 'id'

class ScheduleAppointmentView(generics.CreateAPIView):
    serializer_class = AppointmentListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        doctor_id = self.request.data.get('doctor_id')
        doctor = get_object_or_404(Doctor, user_id=doctor_id)

        appointment_date = self.request.data.get('appointment_date')
        start_time = self.request.data.get('start_time')

        start_datetime = datetime.strptime(start_time, '%H:%M')
        end_datetime = start_datetime + timedelta(minutes=15)

        start_working_hours = datetime.strptime("09:00", '%H:%M')
        end_working_hours = datetime.strptime("18:00", '%H:%M')
        if start_datetime < start_working_hours or end_datetime > end_working_hours:
            raise serializers.ValidationError("Doctor is not available at this time.")

        existing_appointments = Appointment.objects.filter(doctor=doctor, appointment_date=appointment_date)


        serializer.save(
            patient=self.request.user.patient,  # Assuming user has a patient profile
            doctor=doctor,
            start_time=start_datetime.time(),
            end_time=end_datetime.time(),
            is_accepted=False,
        )


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentCreateSerializer