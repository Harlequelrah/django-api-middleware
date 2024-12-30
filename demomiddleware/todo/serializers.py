from .models import ToDo
from rest_framework.serializers import ModelSerializer


class ToDoSerializer(ModelSerializer):
    class Meta:
        model=ToDo
        fields=['id','title','description','is_done','date_created','date_updated']
