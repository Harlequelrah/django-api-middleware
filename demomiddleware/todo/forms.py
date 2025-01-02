from django import forms
from .models import ToDo


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ["title", "description", "is_done"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Enter a title",
                    "required": "required",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Enter a description",
                    "rows": 4,
                    "required": "required",
                }
            ),
            "is_done": forms.CheckboxInput(
                attrs={
                    "class": "w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500",
                }
            ),
        }
