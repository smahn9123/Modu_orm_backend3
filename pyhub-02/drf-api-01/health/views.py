from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from health.models import Todo
from health.serializers import TodoSerializer

#
# @api_view(["GET"])
# def todo_list(request: Request) -> Response:
#     qs = Todo.objects.all()
#     serializer = TodoSerializer(instance=qs, many=True)
#     # 응답포맷은 JSON, XLSX, PNG, PDF, etc.
#     # return JsonResponse(serializer.data, safe=False)  # 동작은 함.
#     return Response(serializer.data)  # 동작은 함.


class TodoViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    # def get_queryset(self):
    #     return super().get_queryset()

    # def get_serializer_class(self):
    #     return super().get_serializer_class()


# /health/todos/  GET
todo_list_or_create = TodoViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)
# /health/todos/  POST
# todo_create = TodoViewSet.as_view({"post": "create"})

# /health/todos/{pk}/
todo_retrieve_or_update_or_delete = TodoViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

# /todos/{pk}/ 주소에 매핑하기
# todo_detail = TodoViewSet.as_view({"get": "retrieve"})
# todo_update = TodoViewSet.as_view({"put": "update"})
# todo_delete = TodoViewSet.as_view({"delete": "destroy"})
