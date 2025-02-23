from django import forms

class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Введите ваше сообщение...'}),
        label=''
    )
