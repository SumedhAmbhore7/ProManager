from django.urls import path
from . import views

urlpatterns = [
    path('create-org/', views.create_organization, name='create_organization'),
    path('settings/', views.team_settings, name='team_settings'),
    path('invite-member/', views.invite_member, name='invite_member'),
]
