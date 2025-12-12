from django.contrib import admin
from .models import SchoolCalendar, NewsEvent, Course, Enrollment, AddDropRequest

@admin.register(SchoolCalendar)
class SchoolCalendarAdmin(admin.ModelAdmin):
    list_display = ('title','start_date','end_date','is_active')

@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title','type','calendar','event_date','created_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code','name','department')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student','course','created_at')

@admin.register(AddDropRequest)
class AddDropRequestAdmin(admin.ModelAdmin):
    list_display = ('student','course','is_add','approved','requested_at')
