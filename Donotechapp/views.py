

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Year, CourseItem
from .forms import CourseForm

def programs(request):
    return render(request, 'programs.html')

def internship(request):
    return render(request, 'internship.html')

def courses(request):
    years = Year.objects.prefetch_related('semesters__course_items').all().order_by('number')
    context = {
        'years': years,
    }
    return render(request, 'courses.html', context)

def jobs(request):
    return render(request, 'jobs.html')

def projects(request):
    return render(request, 'projects.html')

def strategy(request):
    return render(request, 'strategy.html')



@staff_member_required
def course_detail(request, pk):
    course = get_object_or_404(CourseItem, pk=pk)
    return render(request, 'course_detail.html', {'course': course})


@staff_member_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'course_form.html', {'form': form})

@staff_member_required
def course_update(request, pk):
    course = get_object_or_404(CourseItem, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    return render(request, 'course_form.html', {'form': form})

@staff_member_required
def course_delete(request, pk):
    course = get_object_or_404(CourseItem, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses')
    return render(request, 'course_confirm_delete.html', {'course': course})


from .forms import (
    StudentRegistrationForm,
    StudentForm
)


from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from .models import TieUp, StudentExperience, Staff
from django.core.mail import send_mail
from django.conf import settings


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if not name or not email or not message:
            messages.error(request, 'All fields are required.')
        else:
            # Send email to admin
            subject = f"New Contact Form Submission from {name}"
            message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            admin_email = getattr(settings, 'ADMIN_EMAIL', None)
            if admin_email:
                try:
                    send_mail(
                        subject,
                        message_body,
                        settings.EMAIL_HOST_USER,
                        [admin_email],
                        fail_silently=False,
                        # reply_to argument removed due to Django version compatibility
                    )
                except Exception as e:
                    messages.error(request, f"An error occurred while sending your message: {e}")
                    return render(request, 'contact.html')
            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('contact')
    return render(request, 'contact.html')

def home(request):
    context = {
        'institution_name': "DONOTECH SOLUTIONS",
        'institution_details': "DONOTECH SOLUTIONS is a premier placement and training institute dedicated to bridging the gap between academia and industry. We provide cutting-edge training programs and placement assistance to help students launch successful careers in technology.",
        
        'tieups': TieUp.objects.all(),
        'staffs': Staff.objects.all(),
        'experiences': StudentExperience.objects.all(),
    }
    return render(request, 'home.html', context)

logger = logging.getLogger(__name__)

from .models import UserProfile

from .forms import StudentRegistrationForm

def register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                # Create UserProfile
                UserProfile.objects.create(user=user, role='STUDENT')
                # Create Student profile
                student = form.save(commit=False)
                student.user = user
                student.save()
                form.save_m2m()
                messages.success(request, 'Registration successful! You can log in now.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role = request.POST.get('role', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            from .models import Student
            # Try to get or create UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': role})
            if not created and profile.role != role:
                messages.error(request, f"Your account role is '{profile.role}', but you selected '{role}'.")
                return render(request, 'login.html')
            # Validate extra fields for student role and create missing profile if needed
            if role == 'STUDENT':
                student, s_created = Student.objects.get_or_create(user=user)
            login(request, user)
            # Redirect to student dashboard
            if role == 'STUDENT':
                return redirect('student_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


# Separate dashboards for each role
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')


from django.http import HttpResponseForbidden

def role_required(role):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                profile = UserProfile.objects.get(user=request.user)
                if profile.role == role:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden('You are not authorized to view this page.')
            except UserProfile.DoesNotExist:
                return HttpResponseForbidden('User profile not found.')
        return _wrapped_view
    return decorator




@role_required('STUDENT')
def student_dashboard(request):
    from .models import Student
    student_profile = None
    try:
        student_profile = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        pass
    return render(request, 'student_dashboard.html', {'student_profile': student_profile})
# Student details page for admin or staff
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def student_details(request):
    from .models import Student
    students = Student.objects.all()
    return render(request, 'student_details.html', {'students': students})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Student
from .forms import StudentForm
from django.contrib import messages
from django.shortcuts import render

def about_us(request):
    return render(request, 'about_us.html')

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student created successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student_details')
    return render(request, 'student_confirm_delete.html', {'student': student})
