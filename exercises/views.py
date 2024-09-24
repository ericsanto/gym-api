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
    ExerciseListStyleSerializer,
)
from app.permissions import IsAdminOrReadyOnly
from django.db.models import Count
from muscle.models import Muscle


class ExerciseCreateListView(ListCreateAPIView):
    permission_classes = (IsAdminOrReadyOnly,)
    #retorna todos os dados de Exercise
    queryset = Exercise.objects.all()
    #serializer responsável por transformar os dados de Exercise em json
    serializer_class = ExerciseSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    
    #filtra a busca com base em activated_muscle
    filterset_fields = ["activated_muscle"]
    
    #busca por qualquer músculo baseado no nome
    search_fields = ["name"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            #formata e retorna os exercícios em json
            return ExerciseListStyleSerializer
        return ExerciseSerializer

    def create(self, request, *args, **kwargs) -> Response:
        #serializa os dados da requisição
        serializer = self.get_serializer(data=request.data)
        #verifica se os dados são válidos, caso não sejam, retorna uma exceção automaticamente]
        serializer.is_valid(raise_exception=True) 
        #cria um instância da classe Exercise
        self.perform_create(serializer)
        #obtém o cabeçalho HTTP de sucesso para a resposta
        headers = self.get_success_headers(serializer.data)
        """retorna uma mensagem de sucesso, os dados que foram cadastrados,
        o status 201_created e o cabeçalho HTTP"""
        return Response(
            data=({"message": "Exercício criado com sucesso!"}, serializer.data),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

#permite a deleção e update de dados
class ExerciseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    #apenas admistradores pode executar essa ação
    permission_classes = (IsAdminOrReadyOnly,)
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def destroy(self, request, *args, **kwargs) -> Response:
        #captura o objeto que deseja ser deletado ou atualizado
        instance = self.get_object()
        #deleta o objeto capturado
        self.perform_destroy(instance)
        #retorna um dicionário com o status_code_204 e uma mensagem de sucesso
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"message": "Item excluído com sucesso"},
        )


class ExerciceStatsView(APIView):
    queryset = Exercise.objects.all()

    def get(self, request) -> Response:
        try:
            if request.method == "GET":
                total_exercise = self.queryset.count()
                total_muscle = Muscle.objects.all().count()
                exercises_by_muscle = self.queryset.values(
                    "activated_muscle__name"
                ).annotate(number_of_muscle_recruiting_exercises=Count("id"))
                return Response(
                    data={
                        "Total de Exercícios cadastrados": total_exercise,
                        "Total de Músculos cadastrados": total_muscle,
                        "Total de exercícios por músculos": exercises_by_muscle,
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                data={"message": f"Erro ao carregar dados {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
