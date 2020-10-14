import csv
from datetime import datetime
import dateutil
from django.db.models import Prefetch
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import filters
from rest_framework.decorators import action

from apps.authentication.custom_auth import JWTAuthentication
from apps.project.models import Projects, StaffProjects
from apps.staff.models import Staffs, Groups, StaffSkills, Skills, Languages
from apps.staff.serializers import GroupsSerializer, StaffCreateRequestSerializer, \
    StaffCreateResponseSerializer, StaffAllSerializer, \
    ResponseStaffSerializer, RequestStaffSerializer
from apps.utils.views_helper import GenericViewSet
from apps.utils.convert_time import convert_string_to_date


month_param = openapi.Parameter('month', openapi.IN_QUERY, description="month-year", type=openapi.TYPE_STRING)


@method_decorator(name='list', decorator=swagger_auto_schema(manual_parameters=[month_param]))
@method_decorator(name='export_data', decorator=swagger_auto_schema(manual_parameters=[month_param]))
@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
class StaffPlansViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Groups.objects.all()
    action_serializers = {
        "list_response": GroupsSerializer,
        "create_request": StaffCreateRequestSerializer,
        "create_response": StaffCreateResponseSerializer,
        "export_data_response": GroupsSerializer,
    }

    def get_queryset(self):
        current_month = self.request.query_params.get('month')
        if current_month:
            current_date = convert_string_to_date(current_month)
        else:
            current_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        pre_month = current_date - dateutil.relativedelta.relativedelta(months=1)
        next_month = current_date + dateutil.relativedelta.relativedelta(months=2) \
                     - dateutil.relativedelta.relativedelta(days=1)
        print(next_month)
        return Groups.objects.prefetch_related(
            Prefetch(
                "staffs_set",
                queryset=Staffs.objects.prefetch_related(
                    Prefetch(
                        'staffprojects_set',
                        queryset=StaffProjects.objects.filter(
                            start_date__lte=next_month,
                            start_date__gte=pre_month
                        ).annotate(
                            month=TruncMonth('start_date')  # Truncate to month and add to select list
                        ),
                        to_attr="effort"
                    )
                ),
                to_attr="staff"
            )
        )

    def update(self, request, *args, **kwargs):
        pass

    @action(detail=False, methods=['get', ], url_path='export-data')
    def export_data(self, request, *args, **kwargs):
        current_month = self.request.query_params.get('month')
        if current_month:
            current_date = convert_string_to_date(current_month)
        else:
            current_date = datetime.now()

        pre_month = current_date - dateutil.relativedelta.relativedelta(months=1)
        next_month = current_date + dateutil.relativedelta.relativedelta(months=1)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        writer.writerow(['STT', 'Code', 'Name', 'Month {}'.format(pre_month.strftime("%m-%Y")), '',
                         'Month {}'.format(current_date.strftime("%m-%Y")), '',
                         'Month {}'.format(next_month.strftime("%m-%Y")), '',
                         'Action'])
        writer.writerow(['', '', '', 'Project', 'Effort', 'Project', 'Effort', 'Project', 'Effort', ''])

        instance = self.get_response_serializer(self.get_queryset(), many=True).data

        i = 0
        for group in instance:
            groups = []
            if group['leader']:
                groups.extend([group['name'], group['leader']['full_name']])
            else:
                groups.extend([group['name']])
            writer.writerow(groups)
            for staff in group.get('staffs'):
                i = i + 1
                length_arr = 1
                for effort in staff['efforts']:
                    if len(effort['project_staff']) > length_arr:
                        length_arr = len(effort['project_staff'])
                for j in range(length_arr):
                    arr = []
                    if j == 0:
                        arr.extend([i, staff['staff_code'], staff['full_name']])
                    else:
                        arr.extend(['', '', ''])
                    for effort in staff['efforts']:
                        if len(effort['project_staff']) <= j:
                            arr.extend(['', ''])
                        else:
                            project_staff = effort['project_staff'][j]
                            arr.append(project_staff['project']['name'])
                            arr.append(project_staff['effort'])
                    writer.writerow(arr)
        return response


@method_decorator(name='destroy', decorator=swagger_auto_schema(auto_schema=None))
@method_decorator(name='update', decorator=swagger_auto_schema(auto_schema=None))
class StaffViewSet(GenericViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Staffs.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name']

    action_serializers = {
        "list_response": StaffAllSerializer,
        "retrieve_response": StaffAllSerializer,
        "create_request": RequestStaffSerializer,
        "create_response": ResponseStaffSerializer,
        "partial_update_request": RequestStaffSerializer,
        "partial_update_response": ResponseStaffSerializer
    }

    def get_queryset(self):
        return Staffs.objects.prefetch_related(
            Prefetch(
                "languages_set",
                queryset=Languages.objects.all(),
                to_attr="language_set"
            ),
            Prefetch(
                "staffskills_set",
                queryset=StaffSkills.objects.all(),
                to_attr="skill_set"
            )
        )
