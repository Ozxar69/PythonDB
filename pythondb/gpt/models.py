from django.contrib.auth.models import User
from django.db import models


class Dialogue(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dialogues",
        verbose_name="Диалог",
    )
    user_message = models.TextField()
    bot_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Диалог {self.id} пользователя {self.user.username}"
