# hoste_pro/malnad_app/views.py
# malnad_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from .models import Student, Room, Booking
from functools import wraps
from django.db import models

# --- helper decorator for student session auth ---
def student_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.session.get('student_id'):
            return view_func(request, *args, **kwargs)
        messages.info(request, "Please sign in as a student first.")
        return redirect('landing')
    return _wrapped

# --- Landing (combined) ---
def landing(request):
    """
    Combined landing page — student login (USN+name) OR staff login (username+password).
    Redirects to appropriate dashboard after login.
    """
    if request.method == "POST":
        # Student login
        if request.POST.get("student_login") is not None:
            usn = request.POST.get('usn', '').strip()
            name = request.POST.get('name', '').strip()
            if not usn or not name:
                messages.error(request, "Please enter both USN and name.")
                return redirect('landing')
            try:
                student = Student.objects.get(roll_no=usn)
                if student.name.strip().lower() != name.lower():
                    messages.error(request, "USN and name do not match.")
                    return redirect('landing')
                request.session['student_id'] = student.id
                request.session['student_name'] = student.name
                messages.success(request, f"Welcome, {student.name}!")
                return redirect('malnad_app:student_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Student not found. Please check USN.")
                return redirect('landing')

        # Staff login
        if request.POST.get("staff_login") is not None:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                auth_login(request, user)
                messages.success(request, f"Welcome, {user.get_full_name() or user.username}!")
                return redirect('malnad_app:staff_dashboard')
            else:
                messages.error(request, "Staff credentials invalid.")
                return redirect('landing')

    # GET: render landing page with a fresh staff form
    staff_form = AuthenticationForm()
    return render(request, 'landing.html', {"staff_form": staff_form})

# --- Any logout handler (student or staff) ---
def any_logout(request):
    # logout staff
    if request.user.is_authenticated:
        auth_logout(request)
    # clear student session
    request.session.pop('student_id', None)
    request.session.pop('student_name', None)
    messages.info(request, "Signed out.")
    return redirect('landing')

# --- staff logout redirect view (optional) ---
def logout_view(request):
    logout(request)
    return redirect('landing')

# --- Student views ---
@student_required
def student_dashboard(request):
    student_id = request.session.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    bookings = Booking.objects.filter(student=student)
    return render(request, 'student_dashboard.html', {'student': student, 'bookings': bookings})

def student_logout(request):
    request.session.pop('student_id', None)
    request.session.pop('student_name', None)
    messages.info(request, "Signed out.")
    return redirect('landing')

# --- Staff dashboard (Django auth required) ---
@login_required
def staff_dashboard(request):
    # Staff-only stats
    total_students = Student.objects.count()
    total_rooms = Room.objects.count()
    total_bookings = Booking.objects.count()
    available_rooms = Room.objects.filter(capacity__gt=models.F('occupied')).count()
    stats = {
        "total_students": total_students,
        "total_rooms": total_rooms,
        "total_bookings": total_bookings,
        "available_rooms": available_rooms,
    }
    return render(request, 'staff_dashboard.html', {"stats": stats})

# --- Students CRUD (staff) ---
@login_required
def student_list(request):
    students = Student.objects.select_related('room').all().order_by('roll_no')
    return render(request, 'students/list.html', {"students": students})

@login_required
def student_create(request):
    if request.method == "POST":
        roll_no = request.POST.get('roll_no').strip()
        name = request.POST.get('name').strip()
        phone = request.POST.get('phone').strip()
        email = request.POST.get('email').strip()
        room_id = request.POST.get('room') or None
        room = Room.objects.filter(id=room_id).first() if room_id else None

        if Student.objects.filter(roll_no=roll_no).exists():
            messages.error(request, "Student with this USN already exists.")
            return redirect('malnad_app:student_list')

        student = Student.objects.create(roll_no=roll_no, name=name, phone=phone, email=email, room=room)
        if room:
            room.occupied += 1
            room.save(update_fields=['occupied'])
        messages.success(request, f"Student {student.name} added.")
        return redirect('malnad_app:student_list')

    rooms = Room.objects.all()
    return render(request, 'students/create.html', {"rooms": rooms})

# --- Rooms CRUD (staff) ---
@login_required
def room_list(request):
    rooms = Room.objects.all().order_by('number')
    return render(request, 'rooms/list.html', {"rooms": rooms})

@login_required
def room_create(request):
    if request.method == "POST":
        number = request.POST.get('number').strip()
        capacity = int(request.POST.get('capacity') or 1)
        if Room.objects.filter(number=number).exists():
            messages.error(request, "Room already exists.")
            return redirect('malnad_app:room_list')
        room = Room.objects.create(number=number, capacity=capacity, occupied=0)
        messages.success(request, f"Room {room.number} added.")
        return redirect('malnad_app:room_list')
    return render(request, 'rooms/create.html')

# --- Bookings (staff) ---
@login_required
def booking_list(request):
    bookings = Booking.objects.select_related('student', 'room').all()
    return render(request, 'bookings/list.html', {"bookings": bookings})

@login_required
def booking_create(request):
    """
    GET: render booking form with students and rooms.
    POST: validate and create booking, update room occupancy and student's room.
    Always returns an HttpResponse.
    """
    if request.method == "POST":
        student_id = request.POST.get('student')
        room_id = request.POST.get('room')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date') or None

        # Basic validation
        if not student_id or not room_id or not start_date:
            messages.error(request, "Please select a student, a room and a start date.")
            # re-render form with current selections
            students = Student.objects.all()
            rooms = Room.objects.all()
            return render(request, 'bookings/create.html', {"students": students, "rooms": rooms})

        # Ensure objects exist
        try:
            student = Student.objects.get(id=student_id)
            room = Room.objects.get(id=room_id)
        except (Student.DoesNotExist, Room.DoesNotExist):
            messages.error(request, "Selected student or room not found.")
            students = Student.objects.all()
            rooms = Room.objects.all()
            return render(request, 'bookings/create.html', {"students": students, "rooms": rooms})

        # Capacity check
        if room.occupied >= room.capacity:
            messages.error(request, f"Room {room.number} is full.")
            students = Student.objects.all()
            rooms = Room.objects.all()
            return render(request, 'bookings/create.html', {"students": students, "rooms": rooms})

        # Create booking and update occupancy
        Booking.objects.create(student=student, room=room, start_date=start_date, end_date=end_date)
        room.occupied += 1
        room.save(update_fields=['occupied'])

        # Assign room to student (if you want to)
        student.room = room
        student.save(update_fields=['room'])

        messages.success(request, "Booking created.")
        return redirect('malnad_app:booking_list')

    # GET request -> show form
    students = Student.objects.all()
    rooms = Room.objects.all()
    return render(request, 'bookings/create.html', {"students": students, "rooms": rooms})