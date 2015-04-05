from django.db import models
from django.contrib.auth.models import User


class AdminLogs(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=256)

    def __str__(self):
        return self.user.username + ' - ' + self.action + ' - ' + self.date

    class Meta:
        verbose_name_plural = 'logs'
        ordering = ['-date']
