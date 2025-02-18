from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView

from diary.forms import PostForm, CommentForm
from diary.models import Post, Comment


# as_view 함수는 언제 호출되는가 ??
# post_list = ListView.as_view(model=Post)


class PostListView(ListView):
    model = Post
    # template_name = "..."


post_list = PostListView.as_view()


post_detail = DetailView.as_view(model=Post)
# context_data로서 comment_list 쿼리셋을 추가


# post_new = CreateView.as_view(
#     model=Post,
#     form_class=PostForm,
#     success_url=reverse_lazy("diary:post-list"),
# )


def post_new(request):
    if request.method == "POST":
        # form = PostForm(request.POST, request.FILES)
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            # form.cleaned_data
            post = form.save()
            return redirect("diary:post-detail", post.pk)
    else:
        form = PostForm()

    return render(
        request,
        "diary/post_form.html",
        {
            "form": form,
        },
    )


def post_edit(request, pk):
    # try:
    #     post = Post.objects.get(pk=pk)  # Post.DoesNotExist 예외 -> 500 에러
    # except Post.DoesNotExist:
    #     raise Http404

    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        # form = PostForm(request.POST, request.FILES)
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            # form.cleaned_data
            post = form.save()
            return redirect("diary:post-detail", post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "diary/post_form.html",
        {
            "form": form,
        },
    )


class CommentListView(ListView):
    model = Comment

    def get_queryset(self):
        post_pk = self.kwargs["post_pk"]
        qs = super().get_queryset()
        qs = qs.filter(post__pk=post_pk)
        return qs

    # 최종적으로 context 사전값 기반에서 HttpResponse를 생성하는 함수
    def render_to_response(self, context, **response_kwargs):
        fmt = self.request.GET.get("format")
        qs = context["comment_list"]
        if fmt == "json":
            return JsonResponse(list(qs.values()), safe=False)
        # TODO: openpyxl 라이브러리를 직접 활용하여, 쿼리셋 데이터로 엑셀 파일 생성 및 다운로드
        # elif fmt == "xlsx":
        #     pass
        else:
            return super().render_to_response(context, **response_kwargs)


comment_list = CommentListView.as_view()


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "diary/form.html"

    # success_url = reverse_lazy("diary:post-detail", post.pk)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["action_url"] = reverse(
            "diary:comment-new", args=[self.kwargs["post_pk"]]
        )
        return context_data

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])

        # form 인스턴스 내부에 .instance 속성이 있습니다.
        comment = form.save(commit=False)  # instance.save() 호출없이 instance 반환
        comment.post = post
        return super().form_valid(form)

    def get_success_url(self):
        # super().get_success_url()
        created_comment = self.object  # 저장된 모델 인스턴스
        return reverse("diary:post-detail", args=[created_comment.post.pk])


comment_new = CommentCreateView.as_view()
