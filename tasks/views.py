from django.views.generic import ListView

from .models import Task


class TaskView(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'tasks'
    paginate_by = 9
    queryset = Task.objects.order_by('id')

