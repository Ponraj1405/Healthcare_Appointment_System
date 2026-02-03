from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date, parse_time
from django.contrib.auth import authenticate
from .serializers import AppointmentSerializer



from .models import UserProfile, DoctorProfile, Appointment
from .serializers import (
    UserProfileSerializer,
    DoctorProfileSerializer,
    AppointmentSerializer
)


# ------------------ LOGIN ------------------

@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            'status': 'failed',
            'message': 'Invalid username or password'
        })

    try:
        profile = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(profile)

        return Response({
            'status': 'success',
            'data': serializer.data
        })

    except UserProfile.DoesNotExist:
        return Response({
            'status': 'failed',
            'message': 'User profile not found'
        })


# ------------------ DOCTOR LIST ------------------
@api_view(['GET'])
def doctor_list_api(request):
    doctors = DoctorProfile.objects.all()
    serializer = DoctorProfileSerializer(doctors, many=True)

    return Response({
        'status': 'success',
        'data': serializer.data
    })


# ------------------ BOOK APPOINTMENT ------------------
@api_view(['POST'])
def book_appointment_api(request):
    patient_username = request.data.get('patient')
    doctor_username = request.data.get('doctor')
    date = request.data.get('date')
    time = request.data.get('time')

    try:
        patient = User.objects.get(username=patient_username)
        doctor = User.objects.get(username=doctor_username)

        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=parse_date(date),
            time=parse_time(time),
            status='BOOKED'
        )

        serializer = AppointmentSerializer(appointment)

        return Response({
            'status': 'success',
            'data': serializer.data
        })

    except User.DoesNotExist:
        return Response({
            'status': 'failed',
            'message': 'Patient or Doctor not found'
        })

@api_view(['GET'])
def my_appointments_api(request):
    # TEMP: logged-in user
    patient = User.objects.get(username="Ponraj")

    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    serializer = AppointmentSerializer(appointments, many=True)

    return Response({
        'status': 'success',
        'data': serializer.data
    })


@api_view(['GET'])
def appointment_list_api(request):
    patient_username = request.GET.get('patient')

    if not patient_username:
        return Response({
            'status': 'failed',
            'message': 'Patient username required'
        })

    appointments = Appointment.objects.filter(
        patient__username=patient_username
    ).order_by('-created_at')

    serializer = AppointmentSerializer(appointments, many=True)

    return Response({
        'status': 'success',
        'data': serializer.data
    })
