from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint, Student, RoomRequest, ComplaintComment, Fee

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']

class AllocateStudentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(room__isnull=True),
        label="Select Student to Allocate"
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no','contact','course','semester']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title','category','description']

class ComplaintCommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ['comment']

class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = ['preferred_room','reason']

class FeeReceiptForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['amount','receipt_text']  # student enters amount & receipt note
