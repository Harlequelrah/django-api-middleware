from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import ToDo
from .serializers import ToDoSerializer
class ToDoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer
    def get_queryset(self):
        queryset= ToDo.objects.all()
        is_done=self.request.GET.get('is_done')
        if is_done :
            queryset=queryset.filter(is_done=is_done=='True')
        return queryset
