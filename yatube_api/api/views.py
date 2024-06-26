from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет API для модели постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        """Метод API для создания постов."""
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        """Метод API для обновления поста."""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Метод API для удаления поста."""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет API для модели групп постов."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет API для модели комментариев к постам."""

    serializer_class = CommentSerializer

    def get_queryset(self):
        """Метод API для получения querysetа комметариев."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        """Метод API для создания комментария."""
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    def update(self, request, *args, **kwargs):
        """Метод API для обновления комментария."""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Метод API для удаления комментария."""
        instance = self.get_object()
        if instance.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
