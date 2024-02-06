from django.urls import path
from .views import (
    MuscleCreateListView,
    MuscleRetrieveUpdateDestroyView,
)


urlpatterns = [
    path('muscle/', MuscleCreateListView.as_view(), name='muscle_create_list'),
    path('muscle/<int:pk>/', MuscleRetrieveUpdateDestroyView.as_view(),
         name='muscle_retrieve_update_destroy')
]
