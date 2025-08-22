from django.contrib import admin
from .models import UserProfile, Student, CourseItem
from .models import TieUp, StudentExperience, Staff


admin.site.register(TieUp)
admin.site.register(StudentExperience)
admin.site.register(Staff)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email',  'department', 'course_enrolled_display', 'year_semester')

    def course_enrolled_display(self, obj):
        return ", ".join([course.title for course in obj.courses_registered.all()])
    course_enrolled_display.short_description = 'Courses Enrolled'


@admin.register(CourseItem)
class CourseItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'semester', 'description', 'tools')






