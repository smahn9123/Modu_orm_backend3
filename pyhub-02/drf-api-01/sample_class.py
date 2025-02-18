#
# class Person:
#     name = "익명"  # 클래스 변수 (클래스 정의 시점에 실행)
#
#     # 인스턴스 변수는 생성자에서 모아서 정의
#     def __init__(self):
#         print("1)", self.name)  # 클래스 변수를 출력
#         self.name = "Tom"
#         print("2)", self.name)  # 인스턴스 변수를 출력 (CBV의 as_view 메서드에서 활용)
#
# Person()
#
# # print(Person.name)   # 익명
# # print(Person().name) # Tom
# # print(Person.name)   # 익명


# 상속 (다중 상속)

# class A:
#     def say_hello(self):
#         print("Hello from A")
#
# class B:
#     def say_hello(self):
#         print("Hello from B")
#
# class C(A, B):
#     def say_hello(self):
#         super().say_hello()
#
#     # # 부모의 구현을 무시하고, 자식의 구현 만을 동작
#     # def say_hello(self):
#     #     print("Hello from C")
#
# C().say_hello()


class View:
    model = None

    def get_queryset(self):
        return self.model.objects.all()

    def get_template_name(self):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        return f"{app_name}/{model_name}_list.html"

    def get_context_data(self):
        model_name = self.model._meta.model_name
        return {
            f"{model_name}_list": self.get_queryset(),
        }

    @classmethod
    def as_view(cls, model):
        def view(request):
            instance = cls()
            template_name = instance.get_template_name()
            context_data = instance.get_context_data()
            return render(request, template_name, context_data)

        return view


post_list = View.as_view(model=Post)
article_list = View.as_view(model=Article)


def post_list(request):
    qs = Post.objects.all()
    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": qs,
        },
    )


def article_list(request):
    qs = Article.objects.all()
    return render(
        request,
        "blog/article_list.html",
        {
            "article_list": qs,
        },
    )
