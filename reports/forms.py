from django import forms
from .models import ReportTemplate, SavedReport
from projects.models import Project
from defects.models import Defect


class ReportTemplateForm(forms.ModelForm):
    class Meta:
        model = ReportTemplate
        fields = [
            'name', 'report_type', 'description',
            'date_from', 'date_to', 'project',
            'status_filter', 'priority_filter'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'status_filter': forms.Select(attrs={'class': 'form-control'}),
            'priority_filter': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status_filter'].choices = [('', 'Все статусы')] + list(Defect.STATUS_CHOICES)
        self.fields['priority_filter'].choices = [('', 'Все приоритеты')] + list(Defect.PRIORITY_CHOICES)


class ReportFilterForm(forms.Form):
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата с'
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата по'
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Проект'
    )
    status = forms.ChoiceField(
        choices=[('', 'Все статусы')] + list(Defect.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Статус'
    )
    priority = forms.ChoiceField(
        choices=[('', 'Все приоритеты')] + list(Defect.PRIORITY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Приоритет'
    )