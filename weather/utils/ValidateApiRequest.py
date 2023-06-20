from rest_framework.response import Response


class RequestValidate:
    def __init__(self, function_view):
        self.view = function_view

    def __call__(self, request):
        calculate = request.query_params.get('calculate')
        if not calculate:
            data_context = {'code': 101, 'msg': 'calculate parameter should be present', 'results': []}
            return Response(data=data_context, status=400)

        result = self.view(request)
        return result
