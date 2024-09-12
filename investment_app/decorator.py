from functools import wraps
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied


def handle_exceptions(view_func: callable) -> callable:
    """
    Handles exceptions that may occur in the decorated
    view function.

    Args:
        view_func: The view function to be wrapped.

    Returns:
        Response: Returns a response with an error message
          and appropriate status code in case of exceptions.

    Raises:
        None
    """

    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except PermissionDenied as error: 
            return Response(
                {'error': f'Permission Denied, {str(error)}'},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Http404 as error:
            return Response(
                {'error': str(error)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(
                {'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)

    return _wrapped_view