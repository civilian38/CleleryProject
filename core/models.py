from django.db import models

class Chat(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_by_user = models.BooleanField(default=False)

    def __str__(self):
        return ("(USER) " if self.is_by_user else "(ASSISTANT) ") + self.content[:15]