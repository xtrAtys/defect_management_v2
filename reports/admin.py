from django.contrib import admin
from .models import ReportTemplate, SavedReport

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'created_by', 'created_at', 'is_active')
    list_filter = ('report_type', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)

@admin.register(SavedReport)
class SavedReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_template', 'generated_by', 'generated_at', 'file_format')
    list_filter = ('file_format', 'generated_at')
    search_fields = ('name',)
    readonly_fields = ('generated_at',)