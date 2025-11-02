from django.db import models
from django.conf import settings
from django.urls import reverse


class ReportTemplate(models.Model):
    REPORT_TYPE_CHOICES = (
        ('defect', 'Отчет по дефектам'),
        ('project', 'Отчет по проектам'),
        ('user', 'Отчет по пользователям'),
        ('custom', 'Пользовательский отчет'),
    )

    name = models.CharField(max_length=200, verbose_name='Название отчета')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, verbose_name='Тип отчета')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Создатель')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    # Поля фильтрации для отчетов
    date_from = models.DateField(null=True, blank=True, verbose_name='Дата с')
    date_to = models.DateField(null=True, blank=True, verbose_name='Дата по')
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Проект')
    status_filter = models.CharField(max_length=20, blank=True, verbose_name='Фильтр по статусу')
    priority_filter = models.CharField(max_length=20, blank=True, verbose_name='Фильтр по приоритету')

    class Meta:
        verbose_name = 'Шаблон отчета'
        verbose_name_plural = 'Шаблоны отчетов'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('report_detail', kwargs={'pk': self.pk})


class SavedReport(models.Model):
    FORMAT_CHOICES = (
        ('html', 'HTML'),
        ('pdf', 'PDF'),
        ('csv', 'CSV'),
        ('excel', 'Excel'),
    )

    name = models.CharField(max_length=200, verbose_name='Название')
    report_template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, verbose_name='Шаблон отчета')
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Сгенерировал')
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата генерации')
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='html', verbose_name='Формат')
    file_path = models.FileField(upload_to='reports/%Y/%m/%d/', null=True, blank=True, verbose_name='Файл отчета')
    parameters = models.JSONField(default=dict, verbose_name='Параметры отчета')

    class Meta:
        verbose_name = 'Сохраненный отчет'
        verbose_name_plural = 'Сохраненные отчеты'
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.name} ({self.generated_at.strftime('%d.%m.%Y')})"