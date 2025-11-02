from django.contrib import admin
from .models import Project, ProjectStage

class ProjectStageInline(admin.TabularInline):
    model = ProjectStage
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date')
    search_fields = ('name', 'description')
    inlines = [ProjectStageInline]

@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'start_date', 'end_date', 'is_completed')
    list_filter = ('is_completed', 'project')
    search_fields = ('name', 'project__name')