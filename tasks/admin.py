from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'state', 'completed_by', 'completed')
    list_filter = ('state',)

    def completed(self, instance):
        return instance.state == Task.STATE.done

    completed.boolean = True
