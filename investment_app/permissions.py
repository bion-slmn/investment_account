from rest_framework import permissions

class AccountTypePermission(permissions.BasePermission):
    account_permissions = {
        'ACC1': ['GET'], 
        'ACC2': ['GET', 'POST', 'PUT', 'DELETE'],
        'ACC3': ['POST']
    }


    def has_permission(self, request, view):
        """
        This function specifically checks for POST requests and 
        validates the method against the allowed methods for the specified account type.

        Args:
            request: The HTTP request object containing the request method and data.
            view: The view that is being accessed.

        Returns:
            bool: True if the user has permission to perform the action, False otherwise.
        """

        if request.method == 'POST':
            account_type = request.data.get('account_type')
            allowed_methods = self.account_permissions.get(account_type, [])
            return request.method in allowed_methods
        return True

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user has permission to perform a specific action on a given object. 
        Args:
            request: The HTTP request object containing the request method.
            view: The view that is being accessed.
            obj: The object for which permission is being checked.

        Returns:
            bool: True if the request method is allowed 
            for the object's account type, False otherwise.
        """

        account_type = obj.account_type
        allowed_methods = self.account_permissions.get(account_type, [])
        return request.method in allowed_methods
