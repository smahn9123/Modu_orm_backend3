from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response

from diary.models import Post, Comment
from diary.serializers import PostSerializer, CommentSerializer


# @api_view(["POST"])
# def post_new(request: Request) -> Response:
#     serializer = PostSerializer(data=request.data)
#     if serializer.is_valid():
#         post = serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


class PostCreateAPIView(CreateAPIView):
    serializer_class = PostSerializer


post_new = PostCreateAPIView.as_view()

# @api_view(["PUT"])
# def post_edit(request: Request, pk) -> Response:
#     post = get_object_or_404(Post, pk=pk)
#
#     serializer = PostSerializer(data=request.data, instance=post)
#     if serializer.is_valid():
#         post = serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.exclude(status=Post.Status.DELETED)  # 범위
    serializer_class = PostSerializer


post_edit = PostUpdateAPIView.as_view()


class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.exclude(status=Post.Status.DELETED)  # 범위

    # Soft Delete
    def perform_destroy(self, instance: Post):
        # instance.content = ""
        # instance.status = Post.Status.DELETED
        # instance.save()  # 모든 필드 값을 데이터베이스에 UPDATE 시도
        instance.soft_delete()


post_delete = PostDestroyAPIView.as_view()


# def comment_list(request, post_pk):
#     qs = Comment.objects.all()
#     qs = qs.filter(post__pk=post_pk)
#
#     # 커스텀이 어려운 쿼리셋 만을 통한 파이썬 기본 데이터 타입 변환
#     # list(qs.values())
#
#     # QuerySet -> Python 기본 데이터 타입 by Serializer
#     serializer = CommentSerializer(
#         instance=qs,  # QuerySet or Model Instance
#         many=True,  # QuerySet인 경우 True
#     )
#     return JsonResponse(serializer.data, safe=False)


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        qs = super().get_queryset()
        qs = qs.filter(post__pk=post_pk)
        return qs


comment_list = CommentListAPIView.as_view()
