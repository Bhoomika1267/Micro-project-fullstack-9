# hoste_pro/malnad_app/urls.py
# malnad_app/urls.py
from django.urls import path
from . import views

app_name = 'malnad_app'

urlpatterns = [
    # Student session-based pages
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/logout/', views.student_logout, name='student_logout'),

    # Staff / admin protected pages
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),

    # CRUD (staff)
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/add/', views.booking_create, name='booking_create'),

    # optional direct logout for staff
    path('logout/', views.logout_view, name='logout_view'),
]
