from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import timedelta
import csv
import json
from openpyxl import Workbook

from .models import ReportTemplate, SavedReport
from .forms import ReportTemplateForm, ReportFilterForm
from defects.models import Defect
from projects.models import Project
from users.models import CustomUser


@login_required
def dashboard(request):
    """Главная страница отчетов с аналитикой"""

    # Основная статистика
    total_defects = Defect.objects.count()
    open_defects = Defect.objects.filter(status__in=['new', 'in_progress', 'in_review']).count()
    closed_defects = Defect.objects.filter(status='closed').count()
    critical_defects = Defect.objects.filter(priority__in=['high', 'critical']).count()

    # Статистика по статусам
    status_stats = Defect.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')

    # Статистика по приоритетам
    priority_stats = Defect.objects.values('priority').annotate(
        count=Count('id')
    ).order_by('priority')

    # Статистика по проектам
    projects_stats = Project.objects.annotate(
        total_defects=Count('defect'),
        open_defects=Count('defect', filter=Q(defect__status__in=['new', 'in_progress', 'in_review'])),
        closed_defects=Count('defect', filter=Q(defect__status='closed'))
    )[:10]  # Топ 10 проектов

    # Просроченные дефекты
    overdue_defects = Defect.objects.filter(
        due_date__lt=timezone.now().date(),
        status__in=['new', 'in_progress']
    ).count()

    # Активность пользователей (последние 7 дней)
    week_ago = timezone.now() - timedelta(days=7)
    active_users = CustomUser.objects.filter(
        Q(reported_defects__created_at__gte=week_ago) |
        Q(assigned_defects__updated_at__gte=week_ago)
    ).distinct().count()

    context = {
        'total_defects': total_defects,
        'open_defects': open_defects,
        'closed_defects': closed_defects,
        'critical_defects': critical_defects,
        'overdue_defects': overdue_defects,
        'active_users': active_users,
        'status_stats': status_stats,
        'priority_stats': priority_stats,
        'projects_stats': projects_stats,
    }

    return render(request, 'reports/dashboard.html', context)


@login_required
def defect_report(request):
    """Отчет по дефектам с фильтрацией"""

    defects = Defect.objects.all()
    filter_form = ReportFilterForm(request.GET or None)

    if filter_form.is_valid():
        date_from = filter_form.cleaned_data.get('date_from')
        date_to = filter_form.cleaned_data.get('date_to')
        project = filter_form.cleaned_data.get('project')
        status = filter_form.cleaned_data.get('status')
        priority = filter_form.cleaned_data.get('priority')

        if date_from:
            defects = defects.filter(created_at__date__gte=date_from)
        if date_to:
            defects = defects.filter(created_at__date__lte=date_to)
        if project:
            defects = defects.filter(project=project)
        if status:
            defects = defects.filter(status=status)
        if priority:
            defects = defects.filter(priority=priority)

    # Статистика для отчета
    total_count = defects.count()
    avg_resolution_time = defects.filter(resolved_at__isnull=False).aggregate(
        avg_time=Avg('resolved_at' - 'created_at')
    )

    context = {
        'defects': defects,
        'filter_form': filter_form,
        'total_count': total_count,
        'avg_resolution_time': avg_resolution_time['avg_time'] if avg_resolution_time['avg_time'] else 0,
    }

    return render(request, 'reports/defect_report.html', context)


@login_required
def project_report(request):
    """Отчет по проектам"""

    projects = Project.objects.annotate(
        total_defects=Count('defect'),
        open_defects=Count('defect', filter=Q(defect__status__in=['new', 'in_progress', 'in_review'])),
        closed_defects=Count('defect', filter=Q(defect__status='closed')),
        critical_defects=Count('defect', filter=Q(defect__priority__in=['high', 'critical'])),
        avg_resolution_time=Avg('defect__resolved_at' - 'defect__created_at',
                                filter=Q(defect__resolved_at__isnull=False))
    )

    context = {
        'projects': projects,
    }

    return render(request, 'reports/project_report.html', context)


@login_required
def user_report(request):
    """Отчет по пользователям"""

    users = CustomUser.objects.filter(
        Q(role='engineer') | Q(role='manager')
    ).annotate(
        reported_defects_count=Count('reported_defects'),
        assigned_defects_count=Count('assigned_defects'),
        closed_defects_count=Count('assigned_defects', filter=Q(assigned_defects__status='closed')),
        active_defects_count=Count('assigned_defects', filter=Q(assigned_defects__status__in=['new', 'in_progress']))
    )

    context = {
        'users': users,
    }

    return render(request, 'reports/user_report.html', context)


@login_required
def report_templates(request):
    """Список шаблонов отчетов"""

    templates = ReportTemplate.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ReportTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            messages.success(request, 'Шаблон отчета создан успешно!')
            return redirect('report_templates')
    else:
        form = ReportTemplateForm()

    context = {
        'templates': templates,
        'form': form,
    }

    return render(request, 'reports/report_templates.html', context)


@login_required
def export_defects_csv(request):
    """Экспорт дефектов в CSV"""

    defects = Defect.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="defects_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Заголовок', 'Проект', 'Статус', 'Приоритет', 'Исполнитель', 'Срок', 'Создан'])

    for defect in defects:
        writer.writerow([
            defect.id,
            defect.title,
            defect.project.name,
            defect.get_status_display(),
            defect.get_priority_display(),
            defect.assignee.get_full_name() if defect.assignee else 'Не назначен',
            defect.due_date.strftime('%d.%m.%Y') if defect.due_date else '',
            defect.created_at.strftime('%d.%m.%Y %H:%M')
        ])

    return response


@login_required
def export_defects_excel(request):
    """Экспорт дефектов в Excel"""

    defects = Defect.objects.all()

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Дефекты"

    # Заголовки
    headers = ['ID', 'Заголовок', 'Описание', 'Проект', 'Статус', 'Приоритет', 'Исполнитель', 'Срок', 'Создан']
    worksheet.append(headers)

    # Данные
    for defect in defects:
        worksheet.append([
            defect.id,
            defect.title,
            defect.description,
            defect.project.name,
            defect.get_status_display(),
            defect.get_priority_display(),
            defect.assignee.get_full_name() if defect.assignee else 'Не назначен',
            defect.due_date.strftime('%d.%m.%Y') if defect.due_date else '',
            defect.created_at.strftime('%d.%m.%Y %H:%M')
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="defects_report.xlsx"'
    workbook.save(response)

    return response


@login_required
def api_dashboard_stats(request):
    """API для получения статистики для дашборда"""

    # Статистика за последние 30 дней
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Дефекты по дням
    defects_by_day = Defect.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        {'date': "date(created_at)"}
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Статусы дефектов
    status_data = Defect.objects.values('status').annotate(
        count=Count('id')
    )

    data = {
        'defects_by_day': list(defects_by_day),
        'status_data': list(status_data),
    }

    return JsonResponse(data)