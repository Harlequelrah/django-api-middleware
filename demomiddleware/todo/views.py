from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import ToDo
from django.contrib import messages
from .serializers import ToDoSerializer
from .forms import ToDoForm
import httpx

SERVER = "http://localhost:8000/api/todo"


class ToDoViewSet(ModelViewSet):
    serializer_class = ToDoSerializer

    def get_queryset(self):
        queryset = ToDo.objects.all()
        is_done = self.request.GET.get("is_done")
        if is_done:
            queryset = queryset.filter(is_done=is_done == "True")
        return queryset


def get_all_todo(request):
    if request.method == "GET":
        api_url = SERVER + "/"
        with httpx.Client() as client:
            try:
                response = client.get(api_url)
                response.raise_for_status()

                data = response.json()

                serializer = ToDoSerializer(data, many=True)
                return render(
                        request, "todo_list.html", {"todos": serializer.data}
                    )

            except httpx.HTTPStatusError as exc:
                message = (
                    f"HTTP Error: {exc.response.status_code}, "
                    f"details: {exc.response.text}"
                )
                messages.error(request, message)

            except httpx.RequestError as exc:
                message = f"Connection Error: {exc}"
                messages.error(request, message)

        return render(request, "todo_list.html", {"todos": []})


def get_one_todo(request, todo_id: int):
    if request.method == "GET":
        api_url = f"{SERVER}/{todo_id}/"
        with httpx.Client() as client:
            try:
                response = client.get(api_url)
                response.raise_for_status()  # Vérifie les erreurs HTTP (4xx, 5xx) et lance des exceptions  .
                data = response.json()

                serializer = ToDoSerializer(data)
                return render(
                        request, "todo_detail.html", {"todo": serializer.data}
                    )

            except httpx.HTTPStatusError as exc:
                message = (
                    f"HTTP Error: {exc.response.status_code}, "
                    f"details: {exc.response.text}"
                )
                messages.error(request, message)

            except httpx.RequestError as exc:
                message = f"Connection Error: {exc}"
                messages.error(request, message)

        return render(request, "todo_detail.html", {"todo": ToDo()})


async def delete_todo(request, todo_id:int):
    # Requête DELETE à l'API (supposée à l'endpoint 'api/todo/<id>')
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{SERVER}/{todo_id}/")
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            message = (
                f"HTTP Error: {exc.response.status_code}, "
                f"details: {exc.response.text}"
            )
            messages.error(request, message)
        except httpx.RequestError as exc:
            message = f"Connection Error: {exc}"
            messages.error(request, message)
    return redirect("todo_list")

async def update_todo(request, todo_id:int):
    api_url = f"{SERVER}/{todo_id}/"
    with httpx.Client() as client:
        try:
            response = client.get(api_url)
            response.raise_for_status()  # Vérifie les erreurs HTTP (4xx, 5xx) et lance des exceptions  .
            data = response.json()
        except httpx.HTTPStatusError as exc:
            message = (
                f"HTTP Error: {exc.response.status_code}, "
                f"details: {exc.response.text}"
            )
            messages.error(request, message)

        except httpx.RequestError as exc:
            message = f"Connection Error: {exc}"
            messages.error(request, message)

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
            # Requête PUT à l'API (supposée à l'endpoint 'api/todo/<id>')
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.put(api_url, json=json_data)
                    response.raise_for_status()  # Vérifie les erreurs HTTP (4xx, 5xx) et lance des exceptions  .
                    data = response.json()
                except httpx.HTTPStatusError as exc:
                    message = (
                        f"HTTP Error: {exc.response.status_code}, "
                        f"details: {exc.response.text}"
                    )
                    messages.error(request, message)
                except httpx.RequestError as exc:
                    message = f"Connection Error: {exc}"
                    messages.error(request, message)

    else:
        form = ToDoForm(data)

    return render(request, 'todo_update.html', {'form': form})

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
            api_url = f"{SERVER}/"

            # Requête POST à l'API (supposée à l'endpoint 'api/todo')
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(api_url, json=json_data)
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    message = (
                        f"HTTP Error: {exc.response.status_code}, "
                        f"details: {exc.response.text}"
                    )
                    messages.error(request, message)
                except httpx.RequestError as exc:
                    message = f"Connection Error: {exc}"
                    messages.error(request, message)
                return redirect("todo_list")
    else:
        form = ToDoForm()

    return render(request, 'todo/create.html', {'form': form})
