from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.login_api),
    path('api/doctors/', views.doctor_list_api),
    path('api/book-appointment/', views.book_appointment_api),
    path('api/my-appointments/', views.my_appointments_api),
    path('api/appointments/', views.appointment_list_api),


]

