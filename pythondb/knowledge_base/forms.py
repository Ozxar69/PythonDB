from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Для форматирования кода используйте тройные кавычки (```), например:\n\n```python\ndef example():\n    print("Это пример кода")\n```',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("Заголовок не может быть пустым.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("Содержание не может быть пустым.")
        return content
