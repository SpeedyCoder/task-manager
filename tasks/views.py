from distutils.util import strtobool

from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from .models import Task


class TaskListView(ListView):
    model = Task
    template_name = 'tasks_list.html'
    context_object_name = 'tasks'
    paginate_by = 9
    ordering = '-id'

    def get_queryset(self):
        hide_completed = strtobool(self.request.GET.get('hide_completed', 'false'))
        if hide_completed:
            return super().get_queryset().exclude(state=Task.STATE.done)

        return super().get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['hide_completed'] = strtobool(self.request.GET.get('hide_completed', 'false'))

        return context


class TaskCreateView(CreateView):
    model = Task
    template_name = 'create_task.html'
    fields = ('name', 'state', 'description')


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'create_task.html'
    fields = ('name', 'state', 'description')

    def form_valid(self, form):
        if form.instance.state == Task.STATE.done:
            form.instance.completed_by = self.request.user

        return super().form_valid(form)


class MarkAsCompletedView(SingleObjectMixin, View):
    model = Task

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.state != Task.STATE.done:
            instance.state = Task.STATE.done
            instance.completed_by = self.request.user
            instance.save()

        return redirect('home')
