from django.urls import path
from . import views

urlpatterns = [
    # Patient Management URLs
    path('add-patient/', views.add_patient, name='add_patient'),
    path('view-patients/', views.view_patients, name='view_patients'),
    path('edit-patient/<str:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete-patient/<str:patient_id>/', views.delete_patient, name='delete_patient'),

    # Appointment Management URLs
    path('add-appointment/', views.add_appointment, name='add_appointment'),
    path('view-appointments/', views.view_appointments, name='view_appointments'),
    path('edit-appointment/<str:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('delete-appointment/<str:appointment_id>/', views.delete_appointment, name='delete_appointment'),

]