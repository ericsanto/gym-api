from .serializers import MuscleSerializer
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework import status
from .models import Muscle
from app.permissions import IsAdminOrReadyOnly


class MuscleCreateListView(ListCreateAPIView):
    permission_classes = (IsAdminOrReadyOnly,)
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer

    def create(self, request, *args, **kwargs) -> None:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=({"message": "Item criado com sucesso"}, serializer.data),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class MuscleRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadyOnly,)
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer

    def destroy(self, request, *args, **kwargs) -> None:
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            data={"message": "Item deletado com sucesso"},
        )
