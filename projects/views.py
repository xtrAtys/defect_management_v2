from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from users.models import CustomUser


@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {
        'projects': projects
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        try:
            # Создаем проект из данных формы
            project = Project.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                status=request.POST.get('status'),
                manager_id=request.POST.get('manager')
            )
            messages.success(request, 'Проект успешно создан!')
            return redirect('project_list')
        except Exception as e:
            messages.error(request, f'Ошибка при создании проекта: {str(e)}')

    # Получаем список пользователей для выбора менеджера
    users = CustomUser.objects.all()
    return render(request, 'projects/project_form.html', {
        'users': users
    })


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {
        'project': project
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        try:
            project.name = request.POST.get('name')
            project.description = request.POST.get('description')
            project.start_date = request.POST.get('start_date')
            project.end_date = request.POST.get('end_date')
            project.status = request.POST.get('status')
            project.manager_id = request.POST.get('manager')
            project.save()

            messages.success(request, 'Проект успешно обновлен!')
            return redirect('project_detail', pk=project.pk)
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении проекта: {str(e)}')

    users = CustomUser.objects.all()
    return render(request, 'projects/project_form.html', {
        'project': project,
        'users': users
    })