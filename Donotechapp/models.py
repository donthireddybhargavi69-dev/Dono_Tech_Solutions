from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'STUDENT'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')

    def __str__(self):
        return f"{self.user.username} - {self.role}"





# New models for dynamic curriculum

class Year(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Year {self.number}"

class Semester(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='semesters')
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('year', 'number')
        ordering = ['year__number', 'number']

    def __str__(self):
        return f"Year {self.year.number} - Semester {self.number}"

class CourseItem(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='course_items')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tools = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.semester})"


# --- Main Role Models ---
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100, default="Student User")
    email = models.EmailField(default="student@gmail.com")
    phone_number = models.CharField(max_length=20, default="0000000000")
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')], blank=True, default="Other")
    date_of_birth = models.DateField(blank=True, null=True, default=timezone.now)
    college = models.CharField(max_length=255, default="Your Institution Name")
    department = models.CharField(max_length=100, default="Department")
    YEAR_SEMESTER_CHOICES = [
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')
    ]
    year_semester = models.CharField(max_length=17, choices=YEAR_SEMESTER_CHOICES, default='0')
    courses_registered = models.ManyToManyField(CourseItem, blank=True)
    profile_image = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    registration_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Student: {self.user.username}"


from django.db import models
from django_resized import ResizedImageField

class TieUp(models.Model):
    logo = models.ImageField(upload_to='tieups/')

class StudentExperience(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='experiences/')
    quote = models.TextField()

class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    profile_pic = ResizedImageField(size=[300, 300], upload_to='staffs/')
