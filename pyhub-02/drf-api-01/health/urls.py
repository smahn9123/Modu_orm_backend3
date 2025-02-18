from django.urls import path
from . import views

urlpatterns = [
    path("todos/", views.todo_list_or_create),
    path("todos/<int:pk>/", views.todo_retrieve_or_update_or_delete),
    # path("todos/", views.todo_create),
]
