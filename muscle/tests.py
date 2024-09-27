from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Muscle
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView


class MuscleAPITest(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="eric",
            password="12345"
        )
        
        self.url = "/api/v1/muscle/"
        self.muscle_data = {"name" : "Peito"}
        self.token = self.get_token()
        
    def get_token(self):
        response = self.client.post("/api/v1/authentication/token/", {
            "username":"eric",
            "password":"12345"   
        }
        )
        return response.data["access"]
    
        
    def test_create_muscle(self):
        response = self.client.post(
            self.url, 
            self.muscle_data,
            HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Muscle.objects.count(), 1)
        self.assertEqual(Muscle.objects.get().name, "Peito")

    