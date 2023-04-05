from rest_framework.permissions import BasePermission

class IsAuthorOrSuperuser(BasePermission):
    message = 'You must be the author of this post to perform this operation.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
