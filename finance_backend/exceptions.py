from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'status_code': response.status_code,
            'error': _get_error_message(response.data)
        }
        return Response(error_data, status=response.status_code)

    return Response({
        'success': False,
        'status_code': 500,
        'error': 'An unexpected error occurred. Please try again.'
    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_error_message(data):
    if isinstance(data, dict):
        messages = []
        for field, errors in data.items():
            if isinstance(errors, list):
                messages.append(f"{field}: {', '.join(str(e) for e in errors)}")
            else:
                messages.append(f"{field}: {errors}")
        return ' | '.join(messages)

    if isinstance(data, list):
        return ' | '.join(str(e) for e in data)

    return str(data)