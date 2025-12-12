from django.shortcuts import render, get_object_or_404, redirect
from .models import SchoolCalendar, NewsEvent, Course, AddDropRequest, Enrollment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils import timezone
from datetime import date

def home_with_calendar(request):
    # show active calendar items, news and events
    calendars = SchoolCalendar.objects.filter(is_active=True).order_by('-start_date')[:5]
    news = NewsEvent.objects.select_related('calendar').order_by('-created_at')[:10]
    return render(request, 'school_features/home_calendar.html', {'calendars':calendars,'news':news})

@login_required
def add_drop_page(request):
    # assumes user has profile.department and is_head boolean; adapt to project's auth model
    dept = getattr(request.user, 'department', None)
    is_head = getattr(request.user, 'is_department_head', False)
    # only show courses for department head if head; otherwise student's department courses
    if is_head:
        courses = Course.objects.filter(department=dept)
    else:
        courses = Course.objects.all()
    # Restrict by school calendar: only allow add/drop during active calendar date ranges
    today = date.today()
    active_periods = SchoolCalendar.objects.filter(start_date__lte=today, end_date__gte=today, is_active=True)
    allowed = active_periods.exists()
    return render(request, 'school_features/add_drop.html', {'courses':courses,'allowed':allowed})

@login_required
def submit_add_drop(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('POST required')
    course_id = request.POST.get('course_id')
    action = request.POST.get('action')  # 'add' or 'drop'
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'error':'course not found'}, status=404)
    # check calendar
    today = date.today()
    allowed = SchoolCalendar.objects.filter(start_date__lte=today, end_date__gte=today, is_active=True).exists()
    if not allowed:
        return JsonResponse({'error':'Add/Drop not allowed outside calendar dates'}, status=400)
    req = AddDropRequest.objects.create(student=request.user, course=course, is_add=(action=='add'))
    return JsonResponse({'status':'requested','id':req.id})

# Simple API endpoints for dashboard counts (to integrate with frontend charts)
def api_overview_counts(request):
    data = {
        'total_students': getattr(Enrollment.objects, 'count', lambda: Enrollment.objects.count())(),
        'total_courses': Course.objects.count(),
        'total_videos': 0,  # integrate with your media models
        'total_docs': 0,
    }
    return JsonResponse(data)
