from rest_framework import permissions


class CustomPermissionCheck(permissions.BasePermission):

    def has_permission(self, request, view):

      if request.user.is_authenticated:
        if request.user.is_superuser:
          return True
        if request.method == 'GET' :
          return request.user.has_perms(['View'], view.obj_name)
        if request.method == 'PUT' or request.method == 'PATCH':
            return request.user.has_perms(['Edit'], view.obj_name)
        if request.method == 'DELETE':
            return request.user.has_perms(['Delete'], view.obj_name)
        if request.method == 'POST':
            return request.user.has_perms(['Create'], view.obj_name)
        if view.action == 'approve':
            return request.user.has_perms(['Approver'], view.obj_name)
      return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

class IsOwnerOrReadOnlyMessage(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user

class CanDelete(permissions.BasePermission):
    """
    Custom permission to restrict who deletes items
    """

    def has_object_permission(self, request, view, obj):
        # Delete permissions are only allowed to the person who created.
        if request.method == 'DELETE':
            if request.user.is_superuser or (request.user.role and request.user.role.name == 'SUPERADMIN'):
                return True
            return obj.created_by == request.user
        return True
