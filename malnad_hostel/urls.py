from django.urls import path
from . import views

app_name = 'malnad_hostel'

urlpatterns = [
    path('', views.home, name='malnad_home'),

    # Auth
    path('register/', views.register, name='register'),

    # Dashboards
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/management/', views.management_dashboard, name='management_dashboard'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Rooms
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    path('room/<int:pk>/allocate/', views.allocate_to_room, name='allocate_to_room'),
    path('student/<int:student_pk>/unassign/', views.unassign_student, name='unassign_student'),

    # Room requests
    path('request-room/', views.request_room, name='request_room'),
    path('process-room-request/<int:pk>/<str:action>/', views.process_room_request, name='process_room_request'),

    # Complaints
    path('complaint/new/', views.create_complaint, name='create_complaint'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<int:pk>/resolve/', views.resolve_complaint, name='resolve_complaint'),

    # Fees
    path('fees/', views.fees_view, name='fees'),
    path('submit-fee/', views.submit_fee_receipt, name='submit_fee_receipt'),
    path('fee/<int:pk>/verify/', views.verify_fee, name='verify_fee'),
    path('fee/<int:pk>/mark-paid/', views.mark_fee_paid, name='mark_fee_paid'),

    # Mess menu
    path('mess-week/', views.mess_week_view, name='mess_week'),

    # CSV exports
    path('export/students/', views.export_students_csv, name='export_students_csv'),
    path('export/rooms/', views.export_rooms_csv, name='export_rooms_csv'),
    path('export/complaints/', views.export_complaints_csv, name='export_complaints_csv'),
]
