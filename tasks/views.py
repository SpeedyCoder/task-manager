from distutils.util import strtobool

from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.decorators import login_required

from rules.contrib.views import PermissionRequiredMixin

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


class SuccessUrlFromPayloadMixin:

    def get_success_url(self):
        params = self.request.POST.get('redirect_params')
        return f'/?{params}' if params else '/'


class TaskCreateView(SuccessUrlFromPayloadMixin, CreateView):
    model = Task
    template_name = 'create_task.html'
    fields = ('name', 'state', 'description')

    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)


class TaskUpdateView(SuccessUrlFromPayloadMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = 'create_task.html'
    fields = ('name', 'state', 'description')
    permission_required = 'tasks.change_task'

    def form_valid(self, form):
        if form.instance.state == Task.STATE.done:
            form.instance.completed_by = self.request.user

        return super().form_valid(form)


class CompleteView(PermissionRequiredMixin, SingleObjectMixin, View):
    model = Task
    permission_required = 'tasks.change_task'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.state != Task.STATE.done:
            instance.state = Task.STATE.done
            instance.completed_by = self.request.user
            instance.save()

        params = '&'.join(f'{key}={value}' for key, value in self.request.GET.items())

        return redirect(f"/?{params}")


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    model = Task
    permission_required = 'tasks.delete_task'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        params = '&'.join(f'{key}={value}' for key, value in self.request.GET.items())

        return f'/?{params}'


task_list = login_required(TaskListView.as_view())
task_create = login_required(TaskCreateView.as_view())
task_update = login_required(TaskUpdateView.as_view())
task_complete = login_required(TaskUpdateView.as_view())
task_delete = login_required(TaskDeleteView.as_view())
