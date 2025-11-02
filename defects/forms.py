from django import forms
from .models import Defect, DefectComment
from projects.models import Project, ProjectStage
from users.models import CustomUser


class DefectForm(forms.ModelForm):
    class Meta:
        model = Defect
        fields = [
            'title', 'description', 'project', 'stage',
            'priority', 'due_date', 'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'stage': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stage'].queryset = ProjectStage.objects.none()

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['stage'].queryset = ProjectStage.objects.filter(project_id=project_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['stage'].queryset = self.instance.project.stages.all()


class DefectCommentForm(forms.ModelForm):
    class Meta:
        model = DefectComment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class DefectFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'Все статусы')] + list(Defect.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'Все приоритеты')] + list(Defect.PRIORITY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    assignee = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role__in=['engineer', 'manager']),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )