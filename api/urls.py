from django.urls import path
from . import views
from .views import PatientDataView, DoctorDataView, ScheduleAppointmentView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('patient/<int:pk>/', PatientDataView.as_view(), name='patient-detail'),
    path('doctor/<int:pk>/', DoctorDataView.as_view(), name='doctor-detail'),
    path('doctor/<int:doctor_id>/appointment/', ScheduleAppointmentView.as_view(), name='schedule-appointment'),
    # Add more URLs as needed
]