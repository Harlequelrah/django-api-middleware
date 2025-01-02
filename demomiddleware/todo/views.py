from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import ToDo
from .serializers import ToDoSerializer

from django.shortcuts import render, redirect
from .forms import ToDoForm
import httpx 
class ToDoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer
    def get_queryset(self):
        queryset= ToDo.objects.all()
        is_done=self.request.GET.get('is_done')
        if is_done :
            queryset=queryset.filter(is_done=is_done=='True')
        return queryset



async def create_todo(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            # Formulaire valide, transformation des données en JSON
            data = form.cleaned_data
            json_data = {
                'title': data['title'],
                'description': data['description'],
                'is_done': data['is_done'],
            }

            # Requête POST à l'API (supposée à l'endpoint 'api/todo')
            async with httpx.AsyncClient() as client:
                response = await client.post('http://api/todo', json=json_data)

            # Vérifie la réponse de l'API et redirige
            if response.status_code == 201:
                return redirect('todo_list')  

    else:
        form = ToDoForm()

    return render(request, 'todo/create.html', {'form': form})

# async def update_todo(request, id):
#     # Récupère le todo à modifier
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f'http://api/todo/{id}')
#     todo = response.json()

#     if request.method == 'POST':
#         form = ToDoForm(request.POST)
#         if form.is_valid():
#             # Formulaire valide, transformation des données en JSON
#             data = form.cleaned_data
#             json_data = {
#                 'title': data['title'],
#                 'description': data['description'],
#                 'is_done': data['is_done'],
#             }

#             # Requête PUT à l'API (supposée à l'endpoint 'api/todo/<id>')
#             async with httpx.AsyncClient() as client:
#                 response = await client.put(f'http://api/todo/{id}', json=json_data)

#             # Vérifie la réponse de l'API et redirige
#             if response.status_code == 200:
#                 return redirect('todo_list')  # Remplace par l'URL appropriée

#     else:
#         form = ToDoForm(todo)

#     return render(request, 'todo/update.html', {'form': form})

# async def delete_todo(request, id):
    # Requête DELETE à l'API (supposée à l'endpoint 'api/todo/<id>')
    async with httpx.AsyncClient() as client:
        response = await client.delete(f'http://api/todo/{id}')

    # Vérifie la réponse de l'API et redirige
    if response.status_code == 204:
        return redirect('todo_list')  # Remplace par l'URL appropriée

    return redirect('todo_list')  # Remplace par l'URL appropriée       