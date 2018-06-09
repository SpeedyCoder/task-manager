from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('', include('tasks.urls')),
    url(r'^login/$', auth_views.login, dict(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.logout, dict(next_page='/login/'), name='logout'),
    path('admin/', admin.site.urls),
]

admin.site.site_title = 'Task Manager'
admin.site.site_header = 'Task Manager'
