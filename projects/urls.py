from django.urls import path
from .views import ProjectListView, ProjectDetailView, create_task

urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('project/<int:project_id>/create_task/', create_task, name='create_task'),
]
