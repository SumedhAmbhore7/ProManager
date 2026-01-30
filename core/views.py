from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from tasks.models import Task
from teams.models import Membership

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log them in immediately
            return redirect('create_organization') # Send them to create a team
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    my_tasks = Task.objects.filter(assignee=request.user)
    context = {
        'total_tasks': my_tasks.count(),
        'tasks_done': my_tasks.filter(status='DONE').count(),
        'tasks_todo': my_tasks.filter(status='TODO').count(),

        'recent_tasks': my_tasks.order_by('-id')[:3] 
    }
    return render(request, 'core/dashboard.html', context)
