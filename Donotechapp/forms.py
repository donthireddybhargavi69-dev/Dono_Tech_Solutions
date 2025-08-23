from django import forms
from .models import Student, CourseItem, Mentor

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'required': 'required'}))
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', widget=forms.TextInput(attrs={'required': 'required'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'required': 'required'}))
    phone_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'required': 'required'}))
    gender = forms.ChoiceField(choices=[('Male','Male'),('Female','Female'),('Other','Other')], required=True, widget=forms.Select(attrs={'required': 'required'}))
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}))
    college = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'required': 'required'}))
    department = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'required': 'required'}))
    year_semester = forms.ChoiceField(choices=[
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')
    ], required=True, label="Semester", widget=forms.Select(attrs={'required': 'required'}))
    courses_registered = forms.ModelMultipleChoiceField(
        queryset=CourseItem.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'required': 'required'}),
        label="Courses Registered"
    )
    mentor = forms.ModelChoiceField(queryset=Mentor.objects.all(), required=True, empty_label="Select Mentor", widget=forms.Select(attrs={'required': 'required'}))
    
    class Meta:
        model = Student
        fields = [
            'username', 'email', 'phone_number', 'gender', 'date_of_birth',
            'college', 'courses_registered', 'department', 'year_semester', 'profile_image', 'mentor'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required'}),
        }


class StudentForm(forms.ModelForm):
    courses_registered = forms.ModelMultipleChoiceField(
        queryset=CourseItem.objects.all(),
        required=False,
        widget=forms.SelectMultiple,
        label="Courses Registered"
    )
    class Meta:
        model = Student
        fields = [
            'username', 'full_name', 'email', 'phone_number', 'gender', 
            'date_of_birth', 'college', 'courses_registered', 'department',
            'year_semester',  'profile_image'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'year_semester': forms.Select(choices=Student.YEAR_SEMESTER_CHOICES)
        }

class MentorRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
    class Meta:
        model = Mentor
        fields = [
            'username', 'full_name', 'email', 'phone_number',  'profile_image'
        ]

class CourseForm(forms.ModelForm):
    class Meta:
        model = CourseItem
        fields = ['semester', 'title', 'description', 'tools']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tools': forms.Textarea(attrs={'rows': 2}),
        }


