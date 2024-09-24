from django.db import models


class Muscle(models.Model):
    """
    Representa um músculo

    Args:
        name: nome do músculo
        
    Returns:
        _str_: retorna uma string que representa o músculo, que é seu nome
    """
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
