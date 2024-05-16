from django.urls import path
from . import views
from .views import PatientDataView, DoctorDataView, ScheduleAppointmentView, UserAppointmentListView, \
    AppointmentCreateView, AppointmentDetailView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('patient/<int:pk>/', PatientDataView.as_view(), name='patient-detail'),
    path('doctor/<int:pk>/', DoctorDataView.as_view(), name='doctor-detail'),
    path('doctor/<int:doctor_id>/appointment/', ScheduleAppointmentView.as_view(), name='schedule-appointment'),
    path('appointments/', UserAppointmentListView.as_view(), name='user_appointments'),
    path('appointments/create/', AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:id>/', AppointmentDetailView.as_view(), name='appointment_detail')
]