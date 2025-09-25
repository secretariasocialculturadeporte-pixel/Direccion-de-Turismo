from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsTurista(BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios con el rol de TURISTA.
    """
    def has_permission(self, request, view):
        # El usuario debe estar autenticado y tener el rol de TURISTA.
        return bool(request.user and request.user.is_authenticated and request.user.role == CustomUser.Role.TURISTA)


class IsAdminOrFuncionario(BasePermission):
    """
    Permiso personalizado para permitir el acceso solo a usuarios con rol de
    ADMINISTRADOR o FUNCIONARIO.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in [CustomUser.Role.ADMIN, CustomUser.Role.FUNCIONARIO]
        )