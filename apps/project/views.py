import csv
import dateutil
from django.db.models import Prefetch, Sum, Q, Subquery, OuterRef
from datetime import datetime
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import HttpResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from apps.utils.permissions import IsHumanResourceUser, IsAdminUser
from .serializers import *

# Create your views here.
from ..authentication.custom_auth import JWTAuthentication
from ..utils.convert_time import convert_string_to_date
from ..utils.views_helper import GenericViewSet

month_param = openapi.Parameter('month', openapi.IN_QUERY, description="month-year", type=openapi.TYPE_STRING)


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[month_param]))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class ProjectsPlansViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    queryset = Projects.objects.all()
    action_serializers = {
        "create_request": ProjectsPlansCreateRequestSerializer,
        "list_response": ProjectsPlansSerializer,
        "create_response": ProjectsPlansCreateResponseSerializer,
    }
    permission_classes = [IsAdminUser, ]

    def list(self, request, *args, **kwargs):
        current_month = self.request.query_params.get('month')
        if current_month:
            current_date = convert_string_to_date(current_month)
        else:
            current_date = datetime.datetime.now()
        self.queryset = Projects.objects.prefetch_related(
            Prefetch(
                "planprojects_set",
                queryset=PlanProjects.objects.annotate(
                    _actual_effort=Sum("project__staffprojects__effort",
                                       filter=Q(project__staffprojects__start_date__month=ExtractMonth('start_date')) &
                                              Q(project__staffprojects__start_date__year=ExtractYear('start_date')))
                ).filter(start_date__month__lte=current_date.month + 1,
                         start_date__month__gte=current_date.month - 1),
                to_attr="_month_project"
            )
        )
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    @method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[month_param]))
    @action(detail=False, methods=['get', ], url_path='export-data')
    def export_data(self, request, *args, **kwargs):
        querysets = []
        date_month = self.request.query_params.get('month')
        if date_month:
            date_month = convert_string_to_date(date_month).replace(day=1)
        else:
            date_month = datetime.datetime.now().replace(day=1)
        pre_month = date_month - dateutil.relativedelta.relativedelta(months=1)
        next_month = date_month + dateutil.relativedelta.relativedelta(months=1)
        current_date = date_month
        for tmp in range(-1, 2):
            tmp_date = current_date + relativedelta(months=tmp)
            queryset = Projects.objects.annotate(
                actual_effort=Sum("staffprojects__effort",
                                  filter=Q(staffprojects__start_date__month=tmp_date.month)
                                         & Q(staffprojects__start_date__year=tmp_date.year)),
                plan_effort=Subquery(PlanProjects.objects.filter(
                    project=OuterRef('pk'),
                    start_date__month=tmp_date.month
                ).values('plan_effort')[:1])
            ).values_list('project_code', 'name', 'actual_effort', 'plan_effort')
            querysets.append(queryset)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['STT', 'Project Code', 'Project Name', '{}'.format(pre_month.strftime("%m-%Y")), '',
                         '{}'.format(date_month.strftime("%m-%Y")), '',
                         '{}'.format(next_month.strftime("%m-%Y")), ''])
        # for i in enumerate(querysets):
        writer.writerow(['', '', '', 'Actual Effort', 'Plan Effort', 'Actual Effort', 'Plan Effort',
                         'Actual Effort', 'Plan Effort'])
        projects = {}
        i = 0
        for queryset in querysets:
            for item in queryset:
                arr = []
                if item[0] not in projects:
                    i = i + 1
                    arr.append(i)
                    for value in item:
                        arr.append(value)
                else:
                    arr = projects[item[0]]
                    arr.append(item[2])
                    arr.append(item[3])
                projects[item[0]] = arr
        for key in projects.keys():
            writer.writerow(projects[key])
        return response


@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class ProjectsViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    action_serializers = {
        "list_response": ProjectsSerializer,
        "create_request": ProjectCreateRequestsSerializer,
        "create_response": ProjectCreateRequestsSerializer,
        "partial_update_request": ProjectCreateRequestsSerializer,
        "partial_update_response": ProjectCreateRequestsSerializer,
    }
    permission_classes = [IsHumanResourceUser, ]

    def destroy(self, request, *args, **kwargs):
        pass

    @action(detail=False, methods=['get', ], url_path='export-data')
    def export_data(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response, delimiter=',')
        writer.writerow(['Project Code', 'Project Name', 'Project Type', 'Status', 'Start Date', 'End Date',
                         'Team Leader', 'Brse', 'Comtor', 'Created at', 'Update at'])
        projects = Projects.objects.all().values_list('project_code', 'name', 'project_type_id', 'status_id',
                                                      'start_date', 'end_date', 'team_leader__full_name',
                                                      'brse__full_name', 'comtor__full_name', 'created_at',
                                                      'updated_at')
        for project in projects:
            writer.writerow(project)
        return response
