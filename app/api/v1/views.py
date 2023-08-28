from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from . import indexes
from .serializers import SearchQuerySerializer


class Doc(TemplateView):
    template_name = 'doc.html'


class Search(APIView):
    permission_classes = [permissions.AllowAny]
    valid_resource_types = [
        'web_pages',
        'apis',
        'datasets',
        'notebooks',
        None,
        ]

    def get(self, request, resource_type=None):
        if resource_type not in self.valid_resource_types:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SearchQuerySerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        results = indexes.search(
            resource_type,
            serializer.validated_data['q'],
            serializer.validated_data['skip'],
            serializer.validated_data['limit'],
            )

        return Response(results)
