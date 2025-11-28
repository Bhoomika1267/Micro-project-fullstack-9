from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    occupied = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Room {self.number}"

    def is_available(self):
        return self.occupied < self.capacity

class Student(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('warden', 'Warden'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=30, unique=True)
    contact = models.CharField(max_length=20, blank=True)
    course = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=20, blank=True)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.roll_no})"

class RoomRequest(models.Model):
    STATUS_CHOICES = [('pending','Pending'), ('approved','Approved'), ('rejected','Rejected')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    preferred_room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='processed_requests')
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"RoomRequest({self.student}, {self.status})"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    # student submits a short receipt note (no file upload per your request)
    receipt_text = models.TextField(blank=True)
    verified = models.BooleanField(default=False)  # staff can verify

    def __str__(self):
        return f"{self.student} - {self.amount} - {'Paid' if self.paid else 'Pending'}"

class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('cleaning','Cleaning'),
        ('electricity','Electricity'),
        ('water','Water'),
        ('other','Other'),
    ]
    STATUS_CHOICES = [('pending','Pending'), ('in_progress','In Progress'), ('resolved','Resolved')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    response = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student}"

class ComplaintComment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class MessMenu(models.Model):
    date = models.DateField()
    breakfast = models.TextField(blank=True)
    lunch = models.TextField(blank=True)
    dinner = models.TextField(blank=True)

    def __str__(self):
        return f"Menu for {self.date}"
