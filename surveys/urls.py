from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('survey/<int:pk>/', views.survey_detail, name='survey_detail'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('survey/<int:pk>/stats/', views.survey_stats, name='survey_stats'),
    path('survey/<int:pk>/export-csv/', views.export_survey_csv, name='export_survey_csv'),


]
