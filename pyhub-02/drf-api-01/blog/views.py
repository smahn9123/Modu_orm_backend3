# blog/views.py

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post
from .generics import View, APIView


class PostListView(APIView):
    model = Post  # 클래스 변수를 설정

    def get_queryset(self):
        # # 부모의 쿼리셋을 이어받아서 수행
        # qs = super().get_queryset()
        # # qs = qs.filter(...)
        # return qs

        # 자식이 직접 쿼리셋을 생성
        return Post.objects.all()


post_list = PostListView.as_view()

# post_list = View.as_view(model=Post)

# def post_list(request: HttpRequest) -> HttpResponse:
#     post_qs = Post.objects.all()
#     return render(request=request, template_name="blog/post_list.html", context={
#         "post_list": post_qs,
#     })


def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)
    return render(
        request=request,
        template_name="blog/post_detail.html",
        context={
            "post": post,
        },
    )


@login_required
def post_new(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = PostForm()
    else:
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            created_post = form.save(commit=False)
            created_post.author = request.user
            created_post.save()
            return redirect(to="blog:post_detail", pk=created_post.pk)

    return render(
        request=request,
        template_name="blog/post_form.html",
        context={
            "form": form,
        },
    )


@login_required
def post_edit(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        form = PostForm(instance=post)
    else:
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            created_post = form.save()
            return redirect(to="blog:post_detail", pk=created_post.pk)

    return render(
        request=request,
        template_name="blog/post_form.html",
        context={
            "form": form,
            "post": post,
        },
    )


@login_required
def post_delete(request: HttpRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect(to="blog:post_list")

    return render(
        request=request,
        template_name="blog/post_confirm_delete.html",
        context={
            "post": post,
        },
    )
