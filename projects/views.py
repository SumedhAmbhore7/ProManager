from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .models import Project, Task
from .forms import TaskForm

class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object)
        context['form'] = TaskForm()
        return context

def create_task(request, project_id):
    project = Project.objects.get(pk=project_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('project_detail', pk=project_id)
    else:
        form = TaskForm()
    return render(request, 'projects/create_task.html', {'form': form, 'project': project})
