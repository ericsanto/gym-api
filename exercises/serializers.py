from rest_framework import serializers
from .models import Exercise
from muscle.serializers import MuscleSerializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = '__all__'

    def validate_execution(self, value):
        url_validator = URLValidator()

        try:
            url_validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                'A string fornecida não é uma URL')

        return value


class ExerciseListStyleSerializer(serializers.ModelSerializer):
    activated_muscle = MuscleSerializer(many=True)

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'activated_muscle', 'execution',)
