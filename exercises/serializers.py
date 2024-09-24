from rest_framework import serializers
from .models import Exercise
from muscle.serializers import MuscleSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise #modelo que está sendo serializado
        fields = "__all__" #todos os campos do modelo serão serializados

    def validate_execution(self, value):
        
        """Valida o campo 'execution' do modelo Exercise, garantindo que a URL fornecida seja
        seja uma URL válida"""
        
        url_validator = URLValidator() #instancia o validador de URLs do python

        try:
            url_validator(value) 
            #gera um erro no cadastro, caso o campo URL não seja válida
        except ValidationError:
            raise serializers.ValidationError("A string fornecida não é uma URL")

        return value

#define o estilo de como os dados serão retornados
class ExerciseListStyleSerializer(serializers.ModelSerializer):
    activated_muscle = MuscleSerializer(many=True)

    class Meta:
        model = Exercise
        fields = (
            "id",
            "name",
            "activated_muscle",
            "execution",
        )
