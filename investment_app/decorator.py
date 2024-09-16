from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from django.http import (Http404)
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError


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
    exception_mapping = {
            User.DoesNotExist: status.HTTP_404_NOT_FOUND,
            Http404: status.HTTP_404_NOT_FOUND,
            ValidationError: status.HTTP_400_BAD_REQUEST,
            PermissionDenied: status.HTTP_403_FORBIDDEN,
            PermissionError: status.HTTP_403_FORBIDDEN,
        }

    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        """Wraps a view function to handle exceptions and return 
        appropriate HTTP responses.
        """    
        try:
            return view_func(*args, **kwargs)
        except Exception as error:
            status_code = exception_mapping.get(
                type(error),status.HTTP_400_BAD_REQUEST)
            return Response(
                {'error': str(error)}, status=status_code)

    return _wrapped_view