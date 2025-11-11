from django.contrib import admin
from .models import Room, Student, Booking

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'occupied')
    search_fields = ('number',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'room', 'phone')
    search_fields = ('roll_no', 'name')
    list_filter = ('room',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'start_date', 'end_date')
    list_filter = ('room', 'start_date')
    search_fields = ('student__name', 'student__roll_no', 'room__number')
