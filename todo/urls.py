from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('complete/<int:id>/', views.complete_task, name='complete'),
    path('delete/<int:id>/', views.delete_task, name='delete'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
    path('complete/<int:id>/', views.complete_task, name='complete'),
    
]