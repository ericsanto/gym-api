from django.db import models
from muscle.models import Muscle


class Exercise(models.Model):
    """
    Respresenta um exercício físico

    Args:
        name: nome do exercício
        activated_muscle: representa os músculos que são recrutados durante a execução do exercício
        execution: represnta uma URL que redireciona para um vídeo com a execução correta do exercício

    Returns:
        str: retorna uma string que representa o exercício, que é seu nome
    """
    name = models.CharField(max_length=255)
    activated_muscle = models.ManyToManyField(Muscle, related_name="muscle")
    execution = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
