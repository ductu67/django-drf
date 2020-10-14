import calendar
import datetime

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from ProjectsManager import settings
from apps.project.models import *
from apps.utils.convert_time import convert_string_to_date
from apps.utils.error_code import ErrorCode


class PlanEffortSerialiazer(serializers.Serializer):
    month = serializers.SerializerMethodField()
    plan_effort = serializers.SerializerMethodField()
    actual_effort = serializers.SerializerMethodField()

    class Meta:
        fields = ('month', 'plan_effort', 'actual_effort')

    def get_month(self, obj):
        return obj.start_date.strftime("%m/%Y")

    def get_actual_effort(self, obj):
        if obj._actual_effort:
            return round(obj._actual_effort, 2)
        return 0

    def get_plan_effort(self, obj):
        return round(obj.plan_effort, 2)


class ProjectsPlansSerializer(serializers.ModelSerializer):
    efforts = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ('id', 'project_code', 'name', 'status_id', 'efforts')

    def get_efforts(self, obj):
        if hasattr(obj, "_month_project"):
            return PlanEffortSerialiazer(obj._month_project, many=True).data
        return None


class ProjectsPlansCreateRequestSerializer(serializers.ModelSerializer):
    month = serializers.DateField(input_formats=['%m/%Y', ])
    # month = serializers.CharField(required=True)

    class Meta:
        model = PlanProjects
        fields = ('month', 'project', 'plan_effort')

    def validate(self, data):
        current_month = datetime.date.today().replace(day=1)
        if data.get('month') < current_month:
            raise Exception(ErrorCode.validate_month.value)
        if data.get('plan_effort') < 0:
            raise Exception(ErrorCode.validate_plan_effort.value)
        return data

    def save(self, **kwargs):
        # check db co hay ko roi moi tao
        month = self.validated_data["month"]
        project = self.validated_data["project"]
        start_date = month
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        instance = PlanProjects.objects.filter(start_date=start_date, end_date=end_date, project=project)
        if instance.exists():
            instance = instance.first()
            instance.plan_effort = self.validated_data["plan_effort"]
            instance.save()
            return instance
        else:
            instance = PlanProjects.objects.create(
                project=project,
                plan_effort=self.validated_data["plan_effort"],
                start_date=start_date, end_date=end_date)
            return instance


class ProjectsPlansCreateResponseSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = PlanProjects
        fields = ('project', 'month', 'plan_effort')

    def get_month(self, obj):
        return obj.start_date.strftime("%m/%Y")


class StaffSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staffs
        fields = ('id', 'full_name')


class PartnerSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = ("id", "name")


class ProjectsSerializer(serializers.ModelSerializer):
    partner = PartnerSmallSerializer()
    team_leader = StaffSmallSerializer()
    leader = StaffSmallSerializer()
    brse = StaffSmallSerializer()
    comtor = StaffSmallSerializer()

    class Meta:
        model = Projects
        fields = ("id", "project_code", "name", "project_type_id", "status_id", "start_date", "end_date",
                  "partner", "team_leader", "leader", "brse", "comtor", "created_at", "updated_at")
        extra_kwargs = {
            'start_date': {'format': settings.DATE_TIME_INPUT_FORMATS[0]},
            'end_date': {'format': settings.DATE_TIME_INPUT_FORMATS[0]},
            'created_at': {'format': settings.DATE_TIME_INPUT_FORMATS[0]},
            'updated_at': {'format': settings.DATE_TIME_INPUT_FORMATS[0]},

        }

    def validate(self, data):
        if data.get('start_date') > data.get('end_date'):
            raise Exception(ErrorCode.validate_date.value)
        return data


class ProjectCreateRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ("id", "project_code", "name", "project_type_id", "status_id", "start_date", "end_date",
                  "partner", "team_leader", "leader", "brse", "comtor", "created_at", "updated_at")
        extra_kwargs = {
            'start_date': {'input_formats': settings.DATE_INPUT_FORMATS,
                           'format': settings.DATE_TIME_INPUT_FORMATS[0]},
            'end_date': {'input_formats': settings.DATE_INPUT_FORMATS,
                         'format': settings.DATE_TIME_INPUT_FORMATS[0]},
            'created_at': {'format': settings.DATE_TIME_INPUT_FORMATS[0]},
            'updated_at': {'format': settings.DATE_TIME_INPUT_FORMATS[0]},

        }

    def validate(self, data):
        if data.get('start_date') > data.get('end_date'):
            raise Exception(ErrorCode.validate_date.value)
        return data
