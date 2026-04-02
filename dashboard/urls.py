from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('categories/', views.category_breakdown, name='category_breakdown'),
    path('trends/', views.monthly_trend, name='monthly_trend'),
    path('recent/', views.recent_activity, name='recent_activity'),
    path('analytics/', views.analytics, name='analytics'),
]