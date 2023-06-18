from rest_framework import viewsets
from .models import WeatherData
from .serializer import WeatherSerializer
from rest_framework.response import Response

from .utils.pagination_util import paginate_response


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherSerializer

    def get_queryset(self, *args, **kwargs):
        region = kwargs['region']
        return self.queryset.filter(region__in=region, weather_parameter='Tmax')

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset(**request.query_params)
        if instance:
            msg = "Record details fetched successfully."
            resp_data = paginate_response(instance, request, self.serializer_class)
            data_content = {'code': 100, 'msg': msg, 'total_count': resp_data.data['count'],
                            'page_count': len(resp_data.data['results']), 'next': resp_data.data['next'],
                            'previous': resp_data.data['previous'], 'result': resp_data.data['results']}
        else:
            msg = "No Data Present"
            data_content = {'code': 100, 'msg': msg, 'count': 0, 'result': []}
        return Response(data=data_content, status=200)
