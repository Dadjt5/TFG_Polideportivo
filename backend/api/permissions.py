from rest_framework.permissions import BasePermission

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_administrador


class IsMonitor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_monitor


class IsUsuarioFinal(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_usuario_final
