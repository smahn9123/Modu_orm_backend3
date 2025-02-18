from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import serializers
from .models import Post, Comment


class AuthorSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(source="author.name", read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self, author):
        return f"{author.last_name} {author.first_name}"

    class Meta:
        model = get_user_model()
        # model = User
        # fields = "__all__"
        fields = ["id", "username", "email", "name"]


class PostListSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)
    # author = serializers.CharField(source="author.username", read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["pk", "title", "author"]

    @staticmethod
    def get_optimized_queryset():
        return Post.objects.all().defer("content").select_related("author")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["pk", "message"]


class PostDetailSerializer(serializers.ModelSerializer):
    # author = serializers.StringRelatedField(read_only=True)
    # author = serializers.CharField(source="author.username", read_only=True)
    author = AuthorSerializer(read_only=True)

    # comment_list = serializers.StringRelatedField(
    #     many=True, source="comment_set")
    comment_list = CommentSerializer(many=True, read_only=True, source="comment_set")

    @staticmethod
    def get_optimized_queryset():
        return Post.objects.all()

    class Meta:
        model = Post
        fields = ["pk", "title", "content", "author", "comment_list"]
