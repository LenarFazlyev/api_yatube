from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post

MESSAGE: dict = {
    'Post': 'поста',
    'Comment': 'коммента',
}


class IsAuthorOrReadOnly(permissions.BasePermission):
    message = 'Изменение чужого {viewset_class} запрещено!!!'

    def has_object_permission(self, request, view, obj):
        self.message = self.message.format(
            viewset_class=MESSAGE[type(obj).__name__]
        )
        return (obj.author == request.user
                or request.method in permissions.SAFE_METHODS)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]

    def post_get(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        post = self.post_get()
        return post.comments.all()

    def perform_create(self, serializer):
        post = self.post_get()
        serializer.save(author=self.request.user, post=post)
