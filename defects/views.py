from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def defect_list(request):
    return render(request, 'defects/defect_list.html', {
        'message': 'Список дефектов работает!'
    })

@login_required
def defect_create(request):
    return render(request, 'defects/defect_form.html', {
        'message': 'Форма создания дефекта'
    })

@login_required
def defect_detail(request, pk):
    return render(request, 'defects/defect_detail.html', {
        'message': f'Детали дефекта #{pk}'
    })

@login_required
def defect_edit(request, pk):
    return render(request, 'defects/defect_form.html', {
        'message': f'Редактирование дефекта #{pk}'
    })