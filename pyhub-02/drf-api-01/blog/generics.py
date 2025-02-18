from typing import Type

from django.db.models import Model
from django.http import JsonResponse
from django.shortcuts import render


class View:
    model: Type[Model] = None

    def __init__(self, **kwargs):
        # self.model = Post
        # setattr(self, "model", Post)
        for k, v in kwargs.items():
            setattr(self, k, v)  # 인스턴스 변수로서 설정

    def get_queryset(self):
        return self.model.objects.all()

    def get_template_name(self):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return f"{app_name}/{model_name}_list.html"

    def get_context_data(self):
        model_name = self.model._meta.model_name
        return {
            f"{model_name}_list": list(self.get_queryset().values()),
        }

    def dispatch(self, request):
        if request.method == "GET":
            return self.get(request)
        elif request.method == "POST":
            return self.post(request)
        # TODO: 해당 method는 지원하지 않습니다. 라는 오류 응답

    def get(self, request):
        template_name = self.get_template_name()
        context_data = self.get_context_data()
        return self.make_response(request, template_name, context_data)

    def make_response(self, request, template_name, context_data):
        return render(request, template_name, context_data)

    def post(self, request):
        pass

    @classmethod
    def as_view(cls, **initkwargs):
        def view(request):
            instance = cls(**initkwargs)
            return instance.dispatch(request)

        return view


class APIView(View):
    def make_response(self, request, template_name, context_data):
        return JsonResponse(context_data, safe=False)
