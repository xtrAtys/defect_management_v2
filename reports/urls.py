from django.urls import path
from . import views

urlpatterns = [
    # Основные отчеты
    path('', views.dashboard, name='dashboard'),
    path('defects/', views.defect_report, name='defect_report'),
    path('projects/', views.project_report, name='project_report'),
    path('users/', views.user_report, name='user_report'),

    # Шаблоны отчетов
    path('templates/', views.report_templates, name='report_templates'),

    # Экспорт
    path('export/defects/csv/', views.export_defects_csv, name='export_defects_csv'),
    path('export/defects/excel/', views.export_defects_excel, name='export_defects_excel'),

    # API
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
]