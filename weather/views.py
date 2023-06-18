from rest_framework import viewsets
from rest_framework import views
from .models import WeatherData
from .serializer import WeatherSerializer
from rest_framework.response import Response

from .utils.pagination_util import paginate_response


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherSerializer

    def create_query_param(self):
        filter_dict = dict()
        param = self.request.GET
        filter_dict['region__in'] = param.getlist('region')
        filter_dict['year__in'] = param.getlist('year')
        filter_dict['weather_parameter__in'] = param.getlist('weather_parameter')
        return filter_dict

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(**kwargs)

    def list(self, request, *args, **kwargs):
        query_param = self.create_query_param()
        instance = self.get_queryset(**query_param)
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


class RegionParamData(views.APIView):

    def get(self, request) -> Response:
        """
        View to return ann and seasonal weather data for specific region and years
        :param request: Django Request Object
        :return: RestFramework Response.
        """
        query_dict = self.create_query_param()
        model_list = ['region', 'ann', 'weather_parameter', 'year', 'aut', 'sum', 'spr']
        da = WeatherData.objects.only(*model_list).filter(**query_dict).values('year', 'ann', 'aut', 'sum', 'spr')
        data_context = {'code': 100, 'msg': 'Data Got', 'results': da}
        return Response(data=data_context, status=200)

    def create_query_param(self) -> dict:
        """
        Create a dict based on the input that will be used in Model ORM.
        :return: Query Param.
        """
        region = self.request.query_params.get('region')
        weather_param = self.request.query_params.get('weather_param')
        year = self.request.query_params.get('year')
        lower_range_year = self.request.query_params.get('lower_range_year')
        upper_range_year = self.request.query_params.get('upper_range_year')
        lower_range_year = int(lower_range_year) if lower_range_year and lower_range_year.isdigit() else None
        upper_range_year = int(upper_range_year) if upper_range_year and upper_range_year.isdigit() else None
        query_dict = {'region': region, 'weather_parameter': weather_param}
        if year:
            query_dict['year'] = year
        elif lower_range_year and upper_range_year:
            query_dict['year__range'] = [lower_range_year, upper_range_year]
        return query_dict


class RegionYearTemperature(views.APIView):
    def get(self, request):
        query_dict, only_fields = self.create_query_param()
        da = WeatherData.objects.only(*only_fields).filter(**query_dict).values(*only_fields)
        resp = self.process_query_data(da)
        msg = 'Got Data' if resp else 'No Data Present'
        data_context = {'code': 100, 'msg': msg, 'results': resp}
        return Response(data=data_context, status=200)

    def create_query_param(self):
        region = self.request.query_params.get('region')
        year = self.request.query_params.getlist('year')
        # condition_check = {True: lambda x: (int(*x), 'year'), False: lambda x: ([int(i) for i in x], 'year__in')}
        # year, filter_field = condition_check[len(year) == 1](year)
        query_dict = {'region': region, 'weather_parameter__in': ['Tmax', 'Tmin', 'Tmean']}
        if len(year) == 1:
            query_dict['year'] = int(*year)
        elif len(year) > 1:
            query_dict['year__in'] = [int(i) for i in year]
        only_fields = ['weather_parameter', 'year', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep',
                       'oct', 'nov', 'dec']
        return query_dict, only_fields

    def process_query_data(self, query_data):
            t_max = []
            t_min = []
            t_mean = []
            for data in query_data:
                weather_param = data.pop('weather_parameter')
                if weather_param == 'Tmax':
                    t_max.append(data)
                elif weather_param == 'Tmin':
                    t_min.append(data)
                elif weather_param == 'Tmean':
                    t_mean.append(data)
            if t_min and t_mean and t_max:
                resp = {'Tmax': t_max, 'Tmin': t_min, 'Tmean': t_mean}
            else:
                resp = {}
            return resp
