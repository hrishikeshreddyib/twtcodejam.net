from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from TWT.apps.timathon.models import Submission

criteria_validator = [MinValueValidator(1), MaxValueValidator(10)]


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, help_text="The judge")
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        help_text="The submission being judged",
        related_name="votes",
    )

    c1 = models.IntegerField(
        default=1, validators=criteria_validator, help_text="Criterion 1"
    )
    c2 = models.IntegerField(
        default=1, validators=criteria_validator, help_text="Criterion 2"
    )
    c3 = models.IntegerField(
        default=1, validators=criteria_validator, help_text="Criterion 3"
    )
    c4 = models.IntegerField(
        default=1, validators=criteria_validator, help_text="Criterion 4"
    )

    notes = models.TextField(
        max_length=512, null=True, blank=True, help_text="Extra notes"
    )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vote {self.id} for submission {self.submission}."
