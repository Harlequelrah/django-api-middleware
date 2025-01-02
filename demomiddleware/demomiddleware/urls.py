"""
URL configuration for demomiddleware project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from todo.views import ToDoViewSet , get_all_todo , get_one_todo
from rest_framework import routers
from todo import views
router=routers.SimpleRouter()
router.register('todo',ToDoViewSet,basename='todo')
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include(router.urls)),
    path("todo", get_all_todo, name="todo-list"),
    path("todo/<int:todo_id>/", get_one_todo, name="todo-detail"),
    path('create/', views.create_todo, name='create_todo'),
]



