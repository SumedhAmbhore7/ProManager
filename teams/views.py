from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Organization, Membership
from .forms import OrganizationForm, InviteMemberForm
from tasks.models import Task

User = get_user_model()

@login_required
def create_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.owner = request.user
            org.save()

            Membership.objects.create(user=request.user, organization=org, role='admin')

            return redirect('dashboard')
    else:
        form = OrganizationForm()

    return render(request, 'teams/create_org.html', {'form': form})

@login_required
def team_settings(request):
    membership = Membership.objects.filter(user=request.user).first()

    if not membership:
        return redirect('create_organization')

    organization = membership.organization
    members = Membership.objects.filter(organization=organization)
    is_admin = membership.role == 'admin'
    invite_form = InviteMemberForm() if is_admin else None

    tasks = Task.objects.filter(project__organization=organization).order_by('-id')
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='DONE').count()
    in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    todo_tasks = tasks.filter(status='TODO').count()

    completed_percent = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    in_progress_percent = (in_progress_tasks / total_tasks * 100) if total_tasks > 0 else 0
    todo_percent = (todo_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return render(request, 'teams/team_settings.html', {
        'organization': organization,
        'members': members,
        'is_admin': is_admin,
        'invite_form': invite_form,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'todo_tasks': todo_tasks,
        'completed_percent': completed_percent,
        'in_progress_percent': in_progress_percent,
        'todo_percent': todo_percent
    })

@login_required
def invite_member(request):
    membership = get_object_or_404(Membership, user=request.user)

    if membership.role != 'admin':
        messages.error(request, 'Only admins can invite members.')
        return redirect('team_settings')

    if request.method == 'POST':
        form = InviteMemberForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_to_invite = User.objects.get(username=username)
            organization = membership.organization
            if Membership.objects.filter(user=user_to_invite, organization=organization).exists():
                messages.error(request, f'{username} is already a member of the team.')
            else:
                Membership.objects.create(user=user_to_invite, organization=organization, role='member')
                messages.success(request, f'{username} has been invited to the team.')
    else:
        form = InviteMemberForm()

    return redirect('team_settings')
