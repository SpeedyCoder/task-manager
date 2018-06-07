from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from tasks import views

urlpatterns = [
    url(r'^$', login_required(views.TaskListView.as_view()), name='home'),
    url(r'^task/$', login_required(views.TaskCreateView.as_view(success_url="/")), name='tasks-create'),
    url(r'^task/(?P<pk>[\w-]+)$', login_required(views.TaskUpdateView.as_view(success_url="/")), name='tasks-update'),
    url(r'^task/(?P<pk>[\w-]+)/mark_as_completed$',
        login_required(views.MarkAsCompletedView.as_view()), name='tasks-complete'),
    url(r'^login/$', auth_views.login, dict(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.logout, dict(next_page='/login/'), name='logout'),
    path('admin/', admin.site.urls),
]

admin.site.site_title = 'Task Manager'
admin.site.site_header = 'Task Manager'
