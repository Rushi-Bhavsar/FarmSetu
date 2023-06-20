from rest_framework import viewsets
from rest_framework import views
from .models import WeatherData
from .serializer import WeatherSerializer
from rest_framework.response import Response

from .utils.pagination_util import paginate_response
from django.conf import settings
ANNOTATE_SUM_COLUMN_MAPPING = settings.ANNOTATE_SUM_COLUMN_MAPPING
ANNOTATE_AVG_COLUMN_MAPPING = settings.ANNOTATE_AVG_COLUMN_MAPPING


class WeatherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherSerializer

    def create_query_param(self):
        filter_dict = dict()
        param = self.request.GET
        region = param.getlist('region')
        year = param.getlist('year')
        weather_param = param.getlist('weather_parameter')
        if region:
            filter_dict['region__in'] = param.getlist('region')
        if year:
            filter_dict['year__in'] = param.getlist('year')
        if weather_param:
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
        model_list = ['region', 'weather_parameter', 'year', 'ann', 'aut', 'sum', 'spr']
        da = WeatherData.objects.only(*model_list).filter(**query_dict).values(*model_list)
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


def process_query_data(query_data):
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


class RegionYearTemperature(views.APIView):
    def get(self, request):
        query_dict, only_fields = self.create_query_param()
        da = WeatherData.objects.only(*only_fields).filter(**query_dict).values(*only_fields)
        resp = process_query_data(da)
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


def process_region_query_data(region_details):
    resp = {}
    for i in region_details:
        years = [int(i) for i in i.years.split(',')]
        key = i.region
        data = {i.weather_parameter: years}
        if key in resp.keys():
            resp[key].append(data)
        else:
            resp[key] = [data]
    return resp


class GetRegionInfo(views.APIView):
    def get(self, request):
        query_string = "SELECT id, region, weather_parameter, COUNT(year) as no_years, " \
                       "GROUP_CONCAT(year) as years FROM weather_weatherdata GROUP BY region, weather_parameter;"
        region_details = WeatherData.objects.raw(query_string)
        resp_data = process_region_query_data(region_details)
        msg = 'Got Data' if resp_data else 'No Data Present'
        data_context = {'code': 100, 'msg': msg, 'results': resp_data}
        return Response(data=data_context, status=200)


def process_data(data, pop_key):
    data_dict = {}
    for i in data:
        key = i.pop(pop_key)
        if key in data_dict.keys():
            data_dict[key].append(i)
        else:
            data_dict[key] = [i]
    return data_dict


def get_aggregate_filter(calculate, months):
    aggregate_dict = {'sum': ANNOTATE_SUM_COLUMN_MAPPING, 'avg': ANNOTATE_AVG_COLUMN_MAPPING}
    aggregate_func = aggregate_dict[calculate]
    annotate_param = dict()
    for month in months:
        key, value = aggregate_func[month]
        annotate_param[key] = value
    if not annotate_param:
        for k, v in aggregate_func.items():
            key, value = v
            annotate_param[key] = value
    return annotate_param


def get_query_filter(weather_param):
    query_param = dict()
    if weather_param:
        query_param['weather_parameter__in'] = weather_param
    return query_param


class GetData(views.APIView):
    def get(self, request):
        calculate = self.request.query_params.get('calculate')
        months = self.request.query_params.getlist('month')
        weather_param = self.request.query_params.getlist('weather_param')
        annotate_param = get_aggregate_filter(calculate, months)
        query_param = get_query_filter(weather_param)
        data = WeatherData.objects.filter(**query_param).values('region', 'weather_parameter').annotate(**annotate_param)
        resp_data = process_data(data, 'weather_parameter')
        msg = 'Data Got' if resp_data else 'No data'
        data_context = {'code': 100, 'msg': msg, 'results': resp_data}
        return Response(data=data_context, status=200)


class Get2data(views.APIView):
    def get(self, request):
        calculate = self.request.query_params.get('calculate')
        months = self.request.query_params.getlist('month')
        weather_param = self.request.query_params.getlist('weather_param')
        annotate_param = get_aggregate_filter(calculate, months)
        query_param = get_query_filter(weather_param)
        data = WeatherData.objects.filter(**query_param).values('weather_parameter', 'year').annotate(**annotate_param)
        resp_data = process_data(data, 'weather_parameter')
        msg = 'Data Got' if resp_data else 'No data'
        data_context = {'code': 100, 'msg': msg, 'results': resp_data}
        return Response(data=data_context, status=200)


class Fetchdata(views.APIView):
    def get(self, request):
        calculate = self.request.query_params.get('calculate')
        months = self.request.query_params.getlist('month')
        annotate_param = get_aggregate_filter(calculate, months)
        f = dict()
        w_p = self.request.query_params.getlist('weather_param')
        if not w_p:
            msg = 'One weather_parameter is needed.'
            data_context = {'code': 101, 'msg': msg, 'results': []}
            return Response(data=data_context, status=400)
        if len(w_p) == 1:
            f['weather_parameter__in'] = w_p
        else:
            msg = 'Invalid input for weather_parameter. Only one weather_parameter is allowed.'
            data_context = {'code': 101, 'msg': msg, 'results': []}
            return Response(data=data_context, status=400)
        data = WeatherData.objects.filter(**f).values('region', 'year').annotate(**annotate_param)
        resp_data = process_data(data, 'region')
        msg = 'Data Got' if resp_data else 'No data'
        data_context = {'code': 100, 'msg': msg, 'results': resp_data}
        return Response(data=data_context, status=200)
