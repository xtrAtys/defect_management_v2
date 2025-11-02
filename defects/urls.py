from django.urls import path
from . import views

urlpatterns = [
    path('', views.defect_list, name='defect_list'),
    path('create/', views.defect_create, name='defect_create'),
    path('<int:pk>/', views.defect_detail, name='defect_detail'),
    path('<int:pk>/edit/', views.defect_edit, name='defect_edit'),
]