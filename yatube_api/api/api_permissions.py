from rest_framework import permissions

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
