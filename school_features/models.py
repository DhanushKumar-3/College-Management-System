from django.db import models
from django.conf import settings

class SchoolCalendar(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} ({self.start_date} — {self.end_date})"

class NewsEvent(models.Model):
    CAL_TYPE = [('news','News'), ('event','Event')]
    title = models.CharField(max_length=255)
    body = models.TextField()
    type = models.CharField(max_length=10, choices=CAL_TYPE, default='news')
    calendar = models.ForeignKey(SchoolCalendar, on_delete=models.CASCADE, related_name='news_events')
    event_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Course(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=120)
    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)

class AddDropRequest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_add = models.BooleanField(default=True)  # True=Add, False=Drop
    requested_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(null=True)  # None=pending, True/False=decision
    handled_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='handled_adddrops', on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.student} -> {'Add' if self.is_add else 'Drop'} {self.course}"
