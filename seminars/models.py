from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Seminar(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField(null=True)
    location = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class SeminarRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)

    registered_at = models.DateTimeField(auto_now_add=True)
    id_card = models.FileField(upload_to='id_cards/', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'seminar')  # 🚀 prevents duplicate

    def __str__(self):
        return f"{self.user} - {self.seminar}"
