from django.db import models


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "초안"
        PUBLISHED = "published", "Published"
        DELETED = "deleted", "Deleted"

    content = models.TextField()
    photo = models.ImageField(blank=True)  # Pillow 라이브러리 설치가 필요
    status = models.CharField(
        choices=Status.choices,  # 선택지를 제한 !!!
        # default="draft",
        default=Status.DRAFT,
        max_length=20,
    )

    # is_published = models.BooleanField()  # 2가지 값을 가지는 상태

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def soft_delete(self):
        self.content = ""
        self.status = self.Status.DELETED
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # post = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    # post = models.ForeignKey(Post, default=1, on_delete=models.SET_DEFAULT)

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
