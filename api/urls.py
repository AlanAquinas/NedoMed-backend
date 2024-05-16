from django.urls import path
from . import views
from .views import PatientDataView, DoctorDataView, ScheduleAppointmentView, UserAppointmentListView, \
    AppointmentCreateView, AppointmentDetailView, AllDoctorsDataView, UserMedicationsByIDView, \
    UserAnalysisResultsByIDView

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),

    path('patient/<int:pk>/', PatientDataView.as_view(), name='patient-detail'),
    path('patient/<int:id>/medications/', UserMedicationsByIDView.as_view(), name='user_medications_by_id'),
    path('patient/<int:id>/analysis-results/', UserAnalysisResultsByIDView.as_view(), name='user_analysis_results_by_id'),

    path('doctors/<int:pk>/', DoctorDataView.as_view(), name='doctor-detail'),
    path('doctors/', AllDoctorsDataView.as_view(), name='all_doctors'),

    path('appointments/', UserAppointmentListView.as_view(), name='user_appointments'),
    path('appointments/create/', ScheduleAppointmentView.as_view(), name='appointment_create'),
    path('appointments/<int:id>/', AppointmentDetailView.as_view(), name='appointment_detail')
]