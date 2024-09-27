from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Exercise
from muscle.models import Muscle


class MuscleAPITest(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="eric",
            password="12345"
        )
        self.token = self.get_token()
        
        # Criar um músculo que será utilizado nos testes do exercício
        self.muscle = Muscle.objects.create(name="Peito")

    def get_token(self):
        response = self.client.post("/api/v1/authentication/token/", {
            "username": "eric",
            "password": "12345"
        })
        return response.data["access"]
    
    
    
class ExerciseAPITest(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="eric",
            password="12345"
        )
        
        self.token = self.get_token()
        self.muscle = Muscle.objects.create(name="Peito")
        
        self.url = "/api/v1/exercise/"
        self.exercise_data = {"name" : "supino com barra",
                            "activated_muscle" : [
                                self.muscle.id
                            ]
        }
        
    def get_token(self):
        response = self.client.post("/api/v1/authentication/token/", {
            "username":"eric",
            "password":"12345"
        })
        return response.data["access"]
    
    
    def test_create_exercise(self):
        response = self.client.post(
            self.url,
            self.exercise_data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Exercise.objects.get().name, self.exercise_data["name"])
        
    def test_exercise_list(self):
        self.client.post(
            self.url,
            self.exercise_data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Exercise.objects.get().name, self.exercise_data["name"])