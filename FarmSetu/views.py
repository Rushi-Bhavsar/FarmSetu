from rest_framework import status
from django.http import JsonResponse


def handler404(request, exception=None):
    return JsonResponse(data={'error': 'The requested resource is not found'}, status=status.HTTP_404_NOT_FOUND)


def handler403(request, exception=None):
    return JsonResponse(data={'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)


def handler400(request, exception):
    return JsonResponse(data={'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)