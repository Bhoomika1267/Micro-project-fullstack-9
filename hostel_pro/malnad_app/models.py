# hoste_pro/malnad_app/models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Room(models.Model):
    number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    occupied = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.number}"

class Student(models.Model):
    roll_no = models.CharField(max_length=30, unique=True)   # USN
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} -> {self.room} ({self.start_date})"

    class Meta:
        ordering = ['-start_date']
