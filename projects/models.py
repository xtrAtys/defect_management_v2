from django.db import models
from django.conf import settings


class Project(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Планирование'),
        ('active', 'Активный'),
        ('suspended', 'Приостановлен'),
        ('completed', 'Завершен'),
    )

    name = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(blank=True, verbose_name='Описание')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                related_name='managed_projects', verbose_name='Менеджер')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.name


class ProjectStage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages', verbose_name='Проект')
    name = models.CharField(max_length=200, verbose_name='Название этапа')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    is_completed = models.BooleanField(default=False, verbose_name='Завершен')

    class Meta:
        ordering = ['order']
        verbose_name = 'Этап проекта'
        verbose_name_plural = 'Этапы проектов'

    def __str__(self):
        return f"{self.project.name} - {self.name}"