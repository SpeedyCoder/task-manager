from django.conf.urls import url

from tasks import views

urlpatterns = [
    url(r'^$', views.task_list, name='home'),
    url(r'^task/$', views.task_create, name='tasks-create'),
    url(r'^task/(?P<pk>[\w-]+)$', views.task_update, name='tasks-update'),
    url(r'^task/(?P<pk>[\w-]+)/complete$', views.task_complete, name='tasks-complete'),
    url(r'^task/(?P<pk>[\w-]+)/delete$', views.task_delete, name='tasks-delete'),
]
