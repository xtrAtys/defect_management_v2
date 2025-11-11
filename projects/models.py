from django.db import models
from django.conf import settings



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
