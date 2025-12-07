"""
Custom exception handler for Django REST Framework.
Provides comprehensive error logging and user-friendly error messages.
"""
import logging
import traceback
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import Http404

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that logs errors and returns user-friendly messages.
    
    Args:
        exc: The exception that was raised
        context: Context dictionary containing view, request, etc.
    
    Returns:
        Response object with error details
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Get the view and request from context
    view = context.get('view', None)
    request = context.get('request', None)
    
    # Log the error with full context
    log_error(exc, context, response)
    
    # If DRF didn't handle it, handle it ourselves
    if response is None:
        response = handle_unhandled_exception(exc, context)
    else:
        # Enhance DRF's response with user-friendly messages
        response = enhance_error_response(response, exc, context)
    
    return response


def log_error(exc, context, response):
    """
    Log error with full context and stack trace.
    
    Args:
        exc: The exception
        context: Context dictionary
        response: Response object (may be None)
    """
    view = context.get('view', None)
    request = context.get('request', None)
    
    # Build error context
    error_context = {
        'exception_type': type(exc).__name__,
        'exception_message': str(exc),
        'view': view.__class__.__name__ if view else 'Unknown',
        'method': request.method if request else 'Unknown',
        'path': request.path if request else 'Unknown',
        'user': request.user.email if request and hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous',
    }
    
    # Log with stack trace
    logger.error(
        f"API Error: {error_context['exception_type']} in {error_context['view']}",
        extra=error_context,
        exc_info=True
    )
    
    # Log full stack trace for debugging
    logger.debug(f"Stack trace:\n{traceback.format_exc()}")


def handle_unhandled_exception(exc, context):
    """
    Handle exceptions that DRF doesn't handle by default.
    
    Args:
        exc: The exception
        context: Context dictionary
    
    Returns:
        Response object
    """
    # Handle Django's built-in exceptions
    if isinstance(exc, Http404):
        return Response(
            {
                'error': 'Resource not found',
                'detail': 'The requested resource does not exist.',
                'status_code': 404
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    if isinstance(exc, PermissionDenied):
        return Response(
            {
                'error': 'Permission denied',
                'detail': 'You do not have permission to perform this action.',
                'status_code': 403
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    if isinstance(exc, ValidationError):
        return Response(
            {
                'error': 'Validation error',
                'detail': str(exc),
                'status_code': 400
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Handle database errors
    if 'database' in str(exc).lower() or 'sql' in str(exc).lower():
        return Response(
            {
                'error': 'Database error',
                'detail': 'A database error occurred. Please try again later.',
                'status_code': 500
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Handle external API errors
    if 'connection' in str(exc).lower() or 'timeout' in str(exc).lower():
        return Response(
            {
                'error': 'External service error',
                'detail': 'Failed to connect to external service. Please try again later.',
                'status_code': 503
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    
    # Generic server error for anything else
    return Response(
        {
            'error': 'Internal server error',
            'detail': 'An unexpected error occurred. Our team has been notified.',
            'status_code': 500
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def enhance_error_response(response, exc, context):
    """
    Enhance DRF's error response with user-friendly messages.
    
    Args:
        response: DRF's response object
        exc: The exception
        context: Context dictionary
    
    Returns:
        Enhanced response object
    """
    # Add user-friendly error messages based on status code
    if response.status_code == 400:
        if 'error' not in response.data:
            response.data['error'] = 'Invalid request'
        if 'detail' not in response.data and 'non_field_errors' not in response.data:
            response.data['detail'] = 'Please check your input and try again.'
    
    elif response.status_code == 401:
        response.data['error'] = 'Authentication required'
        response.data['detail'] = 'Please log in to access this resource.'
    
    elif response.status_code == 403:
        response.data['error'] = 'Permission denied'
        if 'detail' not in response.data:
            response.data['detail'] = 'You do not have permission to perform this action.'
    
    elif response.status_code == 404:
        response.data['error'] = 'Not found'
        if 'detail' not in response.data:
            response.data['detail'] = 'The requested resource was not found.'
    
    elif response.status_code == 429:
        response.data['error'] = 'Too many requests'
        response.data['detail'] = 'You have made too many requests. Please try again later.'
    
    elif response.status_code >= 500:
        response.data['error'] = 'Server error'
        response.data['detail'] = 'An error occurred on our server. Please try again later.'
    
    # Add status code to response
    response.data['status_code'] = response.status_code
    
    return response


def handle_external_api_error(service_name, error):
    """
    Handle errors from external API services.
    
    Args:
        service_name: Name of the external service (e.g., 'Gemini', 'Replicate')
        error: The error that occurred
    
    Returns:
        User-friendly error message
    """
    logger.error(f"External API error from {service_name}: {str(error)}", exc_info=True)
    
    error_str = str(error).lower()
    
    if 'rate limit' in error_str or '429' in error_str:
        return f"{service_name} rate limit exceeded. Please try again in a few minutes."
    
    if 'timeout' in error_str or 'timed out' in error_str:
        return f"{service_name} request timed out. Please try again."
    
    if 'authentication' in error_str or 'unauthorized' in error_str or '401' in error_str:
        return f"{service_name} authentication failed. Please check API configuration."
    
    if 'not found' in error_str or '404' in error_str:
        return f"Resource not found on {service_name}."
    
    if 'invalid' in error_str or 'bad request' in error_str or '400' in error_str:
        return f"Invalid request to {service_name}. Please check your input."
    
    # Generic error
    return f"{service_name} service is currently unavailable. Please try again later."


def handle_database_error(error):
    """
    Handle database errors with appropriate logging and user messages.
    
    Args:
        error: The database error
    
    Returns:
        User-friendly error message
    """
    logger.error(f"Database error: {str(error)}", exc_info=True)
    
    error_str = str(error).lower()
    
    if 'unique constraint' in error_str or 'duplicate' in error_str:
        return "This record already exists. Please use a different value."
    
    if 'foreign key' in error_str:
        return "Cannot complete operation due to related records."
    
    if 'not null' in error_str:
        return "Required field is missing. Please provide all required information."
    
    if 'connection' in error_str:
        return "Database connection error. Please try again later."
    
    # Generic database error
    return "A database error occurred. Please try again later."
