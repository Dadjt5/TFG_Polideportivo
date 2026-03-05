from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_administrador

class IsAdministradorRaiz(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_administrador_raiz

class IsAdministradorUsuarios(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_administrador_usuarios or request.user.is_administrador_raiz)

class IsAdministradorEspacios(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_administrador_espacios or request.user.is_administrador_raiz)

class IsAdministradorTarifas(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_administrador_tarifas or request.user.is_administrador_raiz)

class IsMonitor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_monitor

class IsUsuarioFinal(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_usuario_final
