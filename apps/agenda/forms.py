from django import forms
from .models import Agenda
from apps.users.models import UserProfile
from django.utils import timezone
from django.core.exceptions import ValidationError


class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ["professor", "aluno", "valor", "data", "hora", "descricao"]

        widgets = {
            "data": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}, format="%Y-%m-%d"
            ),
            "hora": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "descricao": forms.Textarea(
                attrs={
                    "rows": 8,
                    "cols": 40,
                    "class": "form-control",
                    "placeholder": "Exemplo:\n Treino A - Peito:\n - Supino Inclinado 4X10\n - Crucifixo Inclinado 4X10\n - Supino Reto 4X10",
                }
            ),
        }

        labels = {
            "professor": "Nome do Professor(a)",
            "aluno": "Nome do Aluno(a)",
            "valor": "Valor do Treino",
            "data": "Data do Treino",
            "hora": "Horário do Treino",
            "descricao": "Descrição do Treino",
        }

        error_messages = {
            "professor": {
                "required": "O nome do professor é obrigatório.",
            },
            "aluno": {
                "required": "O nome do aluno é obrigatório.",
            },
            "valor": {
                "required": "O valor do treino é obrigatório.",
                "invalid": "Insira um valor válido.",
            },
            "data": {
                "required": "A data do treino é obrigatória.",
            },
            "hora": {
                "required": "A hora do treino é obrigatória.",
            },
            "descricao": {
                "required": "A descrição do treino é obrigatória.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["professor"].queryset = UserProfile.objects.filter(
            is_professor=True
        )

        self.fields["aluno"].queryset = UserProfile.objects.filter(is_professor=False)

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor <= 0:
            raise forms.ValidationError("O valor da aula deve ser maior que zero.")
        return valor

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if data and data < timezone.now().date():
            raise forms.ValidationError("A data do treino não pode ser no passado.")
        return data

    def clean_aluno_e_professor(self):
        cleaned_data = super().clean()
        professor = cleaned_data.get("professor")
        aluno = cleaned_data.get("aluno")

        if professor and not professor.is_professor:
            raise ValidationError(
                "O usuário atribuído como professor não é marcado como professor."
            )

        if aluno and aluno.is_professor:
            raise ValidationError(
                "O usuário atribuído como aluno é marcado como professor."
            )
        return cleaned_data
