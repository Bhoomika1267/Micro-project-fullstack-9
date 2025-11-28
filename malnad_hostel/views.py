# malnad_hostel/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db.models import F
import csv

from .forms import (
    UserRegisterForm, ComplaintForm, ComplaintCommentForm, ProfileForm,
    RoomRequestForm, AllocateStudentForm, FeeReceiptForm
)
from .models import (
    Student, Room, Fee, Complaint, MessMenu,
    RoomRequest, ComplaintComment
)
from django.contrib.auth.models import User


# --- Helpers ---
def is_management(user):
    return user.is_staff


# --- Basic pages ---
def home(request):
    return render(request, 'malnad_hostel/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            roll_no = f"R{user.id:04d}"
            Student.objects.create(user=user, roll_no=roll_no)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('malnad_hostel:student_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'malnad_hostel/register.html', {'form': form})


# --- Student dashboard & profile ---
@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)
    upcoming_menu = MessMenu.objects.order_by('-date')[:7]
    fees = Fee.objects.filter(student=student)
    room_requests = RoomRequest.objects.filter(student=student)
    context = {
        'student': student,
        'upcoming_menu': upcoming_menu,
        'fees': fees,
        'room_requests': room_requests,
    }
    return render(request, 'malnad_hostel/student_dashboard.html', context)


@login_required
def profile_view(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect('malnad_hostel:student_dashboard')
    else:
        form = ProfileForm(instance=student)
    return render(request, 'malnad_hostel/profile.html', {'form': form, 'student': student})


# --- Management dashboard ---
@login_required
@user_passes_test(is_management)
def management_dashboard(request):
    rooms = Room.objects.all()
    complaints = Complaint.objects.filter(status__in=['pending','in_progress']).order_by('-created_at')
    fees = Fee.objects.filter(paid=False)
    room_count = rooms.count()
    student_count = Student.objects.count()
    pending_requests = RoomRequest.objects.filter(status='pending').count()
    pending_fees_count = fees.count()
    context = {
        'rooms': rooms,
        'complaints': complaints,
        'fees': fees,
        'room_count': room_count,
        'student_count': student_count,
        'pending_requests': pending_requests,
        'pending_fees_count': pending_fees_count,
    }
    return render(request, 'malnad_hostel/management_dashboard.html', context)


# --- Room detail / allocation ---
@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # students assigned to this room
    assigned_students = Student.objects.filter(room=room)
    return render(request, 'malnad_hostel/room_detail.html', {'room': room, 'assigned_students': assigned_students})


@login_required
@user_passes_test(is_management)
def allocate_to_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = AllocateStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            if room.is_available():
                student.room = room
                student.save()
                room.occupied = F('occupied') + 1
                room.save()
                # refresh room from DB to update F() expression value
                room.refresh_from_db()
                messages.success(request, f"{student.user.username} allocated to {room.number}")
            else:
                messages.error(request, "Room is full")
            return redirect('malnad_hostel:room_detail', pk=room.pk)
    else:
        form = AllocateStudentForm()
    return render(request, 'malnad_hostel/allocate_to_room.html', {'room': room, 'form': form})


@login_required
@user_passes_test(is_management)
def unassign_student(request, student_pk):
    student = get_object_or_404(Student, pk=student_pk)
    room = student.room
    if room:
        student.room = None
        student.save()
        if room.occupied > 0:
            room.occupied = F('occupied') - 1
            room.save()
            room.refresh_from_db()
        messages.success(request, f"{student.user.username} removed from {room.number}")
    else:
        messages.warning(request, "Student has no room")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('malnad_hostel:management_dashboard')))


# --- Complaints ---
@login_required
def create_complaint(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            comp = form.save(commit=False)
            comp.student = student
            comp.save()
            messages.success(request, "Complaint submitted")
            return redirect('malnad_hostel:student_dashboard')
    else:
        form = ComplaintForm()
    return render(request, 'malnad_hostel/create_complaint.html', {'form': form})


@login_required
def complaint_detail(request, pk):
    comp = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST' and request.user.is_staff:
        form = ComplaintCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.complaint = comp
            comment.author = request.user
            comment.save()
            comp.status = 'in_progress'
            comp.save()
            messages.success(request, "Comment added")
            return redirect('malnad_hostel:complaint_detail', pk=pk)
    else:
        form = ComplaintCommentForm()
    return render(request, 'malnad_hostel/complaint_detail.html', {'complaint': comp, 'form': form})


@login_required
@user_passes_test(is_management)
def resolve_complaint(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    complaint.status = 'resolved'
    complaint.resolved = True
    complaint.save()
    messages.success(request, "Complaint marked resolved")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('malnad_hostel:management_dashboard')))


# --- Fees ---
@login_required
def fees_view(request):
    student = get_object_or_404(Student, user=request.user)
    fees = Fee.objects.filter(student=student)
    return render(request, 'malnad_hostel/fees.html', {'fees': fees})


@login_required
def submit_fee_receipt(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = FeeReceiptForm(request.POST)
        if form.is_valid():
            fee = form.save(commit=False)
            fee.student = student
            fee.paid = False
            fee.verified = False
            fee.save()
            messages.success(request, "Receipt submitted. Wait for verification.")
            return redirect('malnad_hostel:student_dashboard')
    else:
        form = FeeReceiptForm()
    return render(request, 'malnad_hostel/submit_fee_receipt.html', {'form': form})


@login_required
@user_passes_test(is_management)
def mark_fee_paid(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    fee.paid = True
    fee.verified = True
    fee.save()
    messages.success(request, "Fee marked as paid")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('malnad_hostel:management_dashboard')))


@login_required
@user_passes_test(is_management)
def verify_fee(request, pk):
    fee = get_object_or_404(Fee, pk=pk)
    fee.verified = True
    fee.paid = True
    fee.save()
    messages.success(request, "Fee verified and marked paid")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('malnad_hostel:management_dashboard')))


# --- Room requests (student -> management) ---
@login_required
def request_room(request):
    student = get_object_or_404(Student, user=request.user)
    if request.method == 'POST':
        form = RoomRequestForm(request.POST)
        if form.is_valid():
            rr = form.save(commit=False)
            rr.student = student
            rr.save()
            messages.success(request, "Room request submitted")
            return redirect('malnad_hostel:student_dashboard')
    else:
        form = RoomRequestForm()
    return render(request, 'malnad_hostel/request_room.html', {'form': form})


@login_required
@user_passes_test(is_management)
def process_room_request(request, pk, action):
    rr = get_object_or_404(RoomRequest, pk=pk)
    if action == 'approve':
        # try preferred room then fallback to first available
        room = rr.preferred_room if rr.preferred_room and rr.preferred_room.is_available() else Room.objects.filter(occupied__lt=F('capacity')).first()
        if room:
            st = rr.student
            st.room = room
            st.save()
            room.occupied = F('occupied') + 1
            room.save()
            room.refresh_from_db()
            rr.status = 'approved'
            rr.processed_by = request.user
            rr.processed_at = timezone.now()
            rr.save()
            messages.success(request, "Request approved and student allocated")
        else:
            messages.error(request, "No available room to allocate")
    elif action == 'reject':
        rr.status = 'rejected'
        rr.processed_by = request.user
        rr.processed_at = timezone.now()
        rr.save()
        messages.success(request, "Request rejected")
    return redirect('malnad_hostel:management_dashboard')


# --- Mess menu ---
@login_required
def mess_week_view(request):
    today = timezone.localdate()
    days = [today + timezone.timedelta(days=i) for i in range(7)]
    menus = {m.date: m for m in MessMenu.objects.filter(date__in=days)}
    ordered = [(d, menus.get(d)) for d in days]
    return render(request, 'malnad_hostel/mess_week.html', {'ordered': ordered})


# --- CSV exports ---
@login_required
@user_passes_test(is_management)
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(response)
    writer.writerow(['username','full_name','roll_no','contact','course','semester','room'])
    for s in Student.objects.select_related('user','room').all():
        writer.writerow([s.user.username, s.user.get_full_name(), s.roll_no, s.contact, s.course, s.semester, s.room.number if s.room else ''])
    return response


@login_required
@user_passes_test(is_management)
def export_rooms_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rooms.csv"'
    writer = csv.writer(response)
    writer.writerow(['number','capacity','occupied'])
    for r in Room.objects.all():
        writer.writerow([r.number, r.capacity, r.occupied])
    return response


@login_required
@user_passes_test(is_management)
def export_complaints_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="complaints.csv"'
    writer = csv.writer(response)
    writer.writerow(['title','student','category','status','created_at'])
    for c in Complaint.objects.select_related('student__user').all():
        writer.writerow([c.title, c.student.user.username, c.category, c.status, c.created_at])
    return response
