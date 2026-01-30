from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'due_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'assignee': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        # We need to filter the assignees so you can't assign a task to someone in a DIFFERENT company
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if organization:
            from teams.models import Membership
            # Find users who are members of this organization
            members = Membership.objects.filter(organization=organization).values_list('user__id', flat=True)
            from django.contrib.auth import get_user_model
            User = get_user_model()
            self.fields['assignee'].queryset = User.objects.filter(id__in=members)
