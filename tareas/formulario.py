from django import forms
from .models import Tareas

class formulario_tarea(forms.ModelForm):
    class Meta:
        model = Tareas
        fields= ['title','description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Escribe un titulo"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Escribe una descripcion"}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }