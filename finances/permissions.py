from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Classe de permissão personalizada para verificar se o usuário autenticado é
    o proprietário de um determinado objeto.

    Atributos:
        Nenhum atributo específico nesta classe.

    Métodos:
        has_object_permission: Verifica se o usuário autenticado é o
        proprietário do objeto fornecido.
        has_permission: Verifica se o usuário tem permissão para acessar o
        objeto.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifica se o usuário autenticado é o proprietário do objeto fornecido.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            view: A view que está sendo acessada.
            obj: O objeto específico que está sendo acessado.

        Retorna:
            bool: True se o usuário for o proprietário do objeto, False caso
            contrário.
        """
        return obj.account.owner == request.user

    def has_permission(self, request, view):
        """
        Verifica se o usuário tem permissão para acessar o objeto.

        Parâmetros:
            request: O objeto da solicitação HTTP.
            view: A view que está sendo acessada.

        Retorna:
            bool: True se o usuário tiver permissão para acessar o objeto,False
            caso contrário.
        """
        return super().has_permission(request, view)
