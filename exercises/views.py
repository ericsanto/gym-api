from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import status
from .models import Exercise
from .serializers import (
    ExerciseSerializer,
    ExerciseListStyleSerializer
)
from app.permissions import IsAdminOrReadyOnly
from django.db.models import Count


class ExerciseCreateListView(ListCreateAPIView):
    permission_classes = (IsAdminOrReadyOnly,)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['activated_muscle']
    search_fields = ['name']

    def get_serializer_class(self) -> None:
        if self.request.method == 'GET':
            return ExerciseListStyleSerializer
        return ExerciseSerializer

    def create(self, request, *args, **kwargs) -> None:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data=({"message": "Exercício criado com sucesso!"},
                              serializer.data),
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class ExerciseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadyOnly,)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def destroy(self, request, *args, **kwargs) -> None:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={"message": "Item excluído com sucesso"})


class ExerciceStatsView(APIView):
    queryset = Exercise.objects.all()

    def get(self, request) -> None:
        try:
            if request.method == 'GET':
                total_exercise = self.queryset.count()
                exercises_by_muscle = self.queryset.values(
                    'activated_muscle__name').annotate(count=Count('id'))
                return Response(data={'Total de Exercícios cadastrados': total_exercise,
                                      'Total de exercícios por músculos': exercises_by_muscle},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'message': f'Erro ao carregar dados {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
