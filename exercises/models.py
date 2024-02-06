from django.db import models
from muscle.models import Muscle


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    activated_muscle = models.ManyToManyField(
        Muscle, related_name='muscle')

    def __str__(self) -> str:
        return self.name
