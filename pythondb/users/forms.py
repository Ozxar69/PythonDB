from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import EmailField

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('first_name', 'username', 'email')


class ResetPasswordForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email не найден.")
        return email
