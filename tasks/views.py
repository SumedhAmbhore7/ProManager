from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Task
from .forms import ProjectForm, TaskForm
from teams.models import Membership

@login_required
def project_list(request):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership:
        messages.error(request, "You are not a member of any organization.")
        return redirect('core:dashboard')

    projects = Project.objects.filter(organization=membership.organization)
    return render(request, 'tasks/project_list.html', {
        'projects': projects,
        'user_role': membership.role,
    })

@login_required
def create_project(request):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership or membership.role != 'admin':
        messages.error(request, "You do not have permission to create projects.")
        return redirect('tasks:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.organization = membership.organization
            project.save()
            messages.success(request, "Project created successfully.")
            return redirect('tasks:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    return render(request, 'tasks/create_project.html', {'form': form})

@login_required
def project_detail(request, pk):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership:
        messages.error(request, "You are not a member of any organization.")
        return redirect('core:dashboard')

    # Security: Ensure project belongs to user's org
    project = get_object_or_404(Project, pk=pk, organization=membership.organization)

    # Separation for Kanban Columns
    tasks_todo = project.tasks.filter(status='TODO')
    tasks_inprogress = project.tasks.filter(status='IN_PROGRESS')
    tasks_done = project.tasks.filter(status='DONE')

    return render(request, 'tasks/project_detail.html', {
        'project': project,
        'tasks_todo': tasks_todo,
        'tasks_inprogress': tasks_inprogress,
        'tasks_done': tasks_done,
        'user_role': membership.role,
    })

@login_required
def create_task(request, project_id):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership:
        messages.error(request, "You are not a member of any organization.")
        return redirect('core:dashboard')

    project = get_object_or_404(Project, pk=project_id, organization=membership.organization)

    if request.method == 'POST':
        form = TaskForm(request.POST, organization=membership.organization)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, "Task created successfully.")
            return redirect('tasks:project_detail', pk=project.pk)
    else:
        form = TaskForm(organization=membership.organization)
    return render(request, 'tasks/create_task.html', {'form': form, 'project': project})

@login_required
def assign_task(request, task_id):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership:
        messages.error(request, "You are not a member of any organization.")
        return redirect('core:dashboard')

    task = get_object_or_404(Task, pk=task_id, project__organization=membership.organization)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, organization=membership.organization)
        if form.is_valid():
            form.save()
            messages.success(request, "Task assigned successfully.")
            return redirect('tasks:project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task, organization=membership.organization)
    return render(request, 'tasks/assign_task.html', {'form': form, 'task': task})

@login_required
def update_task_status(request, task_id):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership:
        messages.error(request, "You are not a member of any organization.")
        return redirect('core:dashboard')

    task = get_object_or_404(Task, pk=task_id, project__organization=membership.organization)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            messages.success(request, "Task status updated successfully.")
        else:
            messages.error(request, "Invalid status.")
    return redirect('tasks:project_detail', pk=task.project.pk)

@login_required
def edit_project(request, pk):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership or membership.role != 'admin':
        messages.error(request, "You do not have permission to edit projects.")
        return redirect('tasks:project_list')

    project = get_object_or_404(Project, pk=pk, organization=membership.organization)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect('tasks:project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'tasks/edit_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    membership = Membership.objects.filter(user=request.user).first()
    if not membership or membership.role != 'admin':
        messages.error(request, "You do not have permission to delete projects.")
        return redirect('tasks:project_list')

    project = get_object_or_404(Project, pk=pk, organization=membership.organization)

    if request.method == 'POST':
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect('tasks:project_list')
    return render(request, 'tasks/delete_project.html', {'project': project})
