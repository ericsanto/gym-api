from rest_framework.permissions import BasePermission


SAFE_METHODS = (
    "GET",
    "HEAD",
    "OPTIONS",
)


class IsAdminOrReadyOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        return bool(
            request.method in SAFE_METHODS or (request.user and request.user.is_staff)
        )
