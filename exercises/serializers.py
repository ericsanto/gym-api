from rest_framework import serializers
from .models import Exercise
from muscle.serializers import MuscleSerializer


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = '__all__'


class ExerciseListStyleSerializer(serializers.ModelSerializer):
    activated_muscle = MuscleSerializer(many=True)

    class Meta:
        model = Exercise
        fields = ('id', 'name', 'activated_muscle',)
