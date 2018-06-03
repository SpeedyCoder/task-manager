from django.views.generic import CreateView
from django.views.generic import ListView

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'
    paginate_by = 9
    queryset = Task.objects.order_by('-id')


class TaskCreateView(CreateView):
    model = Task
    template_name = 'create_task.html'
    fields = ('name', 'description')
