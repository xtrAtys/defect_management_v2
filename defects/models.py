from django.db import models
from django.conf import settings


class Defect(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('in_review', 'На проверке'),
        ('closed', 'Закрыта'),
        ('cancelled', 'Отменена'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический'),
    )

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, verbose_name='Проект')
    stage = models.ForeignKey('projects.ProjectStage', on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='Этап')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_name='reported_defects', verbose_name='Автор')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='assigned_defects', verbose_name='Исполнитель')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='Приоритет')
    due_date = models.DateField(null=True, blank=True, verbose_name='Срок исправления')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Дефект'
        verbose_name_plural = 'Дефекты'

    def __str__(self):
        return self.title


class DefectAttachment(models.Model):
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE, related_name='attachments', verbose_name='Дефект')
    file = models.FileField(upload_to='defect_attachments/%Y/%m/%d/', verbose_name='Файл')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Загрузил')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'

    def __str__(self):
        return f"Вложение для {self.defect.title}"


class DefectComment(models.Model):
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE, related_name='comments', verbose_name='Дефект')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f"Комментарий от {self.author}"


class DefectHistory(models.Model):
    defect = models.ForeignKey(Defect, on_delete=models.CASCADE, related_name='history', verbose_name='Дефект')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кто изменил')
    change_description = models.TextField(verbose_name='Описание изменения')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')

    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'История изменений'
        verbose_name_plural = 'История изменений'

    def __str__(self):
        return f"Изменение {self.defect.title}"