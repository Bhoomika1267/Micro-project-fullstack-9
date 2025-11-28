from django.contrib import admin
from .models import Student, Room, Fee, Complaint, MessMenu, RoomRequest, ComplaintComment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'room')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'occupied', 'is_available')
    readonly_fields = ('is_available',)

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'paid', 'timestamp')
    list_filter = ('paid',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'resolved', 'created_at')
    list_filter = ('resolved',)

@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ('date',)
admin.site.register(RoomRequest)
admin.site.register(ComplaintComment)