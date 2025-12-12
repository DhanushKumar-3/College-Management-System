from django.urls import path
from . import views

app_name = 'school_features'

urlpatterns = [
    path('', views.home_with_calendar, name='home_calendar'),
    path('add-drop/', views.add_drop_page, name='add_drop'),
    path('submit-add-drop/', views.submit_add_drop, name='submit_add_drop'),
    path('api/overview/', views.api_overview_counts, name='api_overview'),
]
