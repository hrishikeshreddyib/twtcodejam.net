from django.db import models
from django.contrib.auth.models import User


class Timer(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    title = models.TextField(
        help_text="Title for the timer"
    )
    date_time = models.DateTimeField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Creator"
    )
