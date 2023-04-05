from rest_framework.permissions import BasePermission

class IsOwnerOrSuperuser(BasePermission):
    message = 'You must be the owner of this comment to perform this operation.'

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_superuser
