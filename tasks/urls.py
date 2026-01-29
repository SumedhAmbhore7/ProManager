from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('project_list/', views.project_list, name='project_list'),
    path('create/', views.create_project, name='create_project'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('<int:project_id>/create-task/', views.create_task, name='create_task'),
    path('task/<int:task_id>/assign/', views.assign_task, name='assign_task'),
    path('task/<int:task_id>/update/', views.update_task_status, name='update_task_status'),
]
