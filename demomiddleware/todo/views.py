from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import ToDo
from .serializers import ToDoSerializer
class ToDoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer
    def get_queryset(self):
        return ToDo.objects.all()
