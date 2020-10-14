from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from rest_framework import serializers
from apps.staff.models import Staffs, Groups, DeveloperTypes, Ranks, StaffSkills, Skills, Languages
from apps.project.models import StaffProjects, Projects
from apps.utils.convert_time import convert_string_to_date
from apps.utils.error_code import ErrorCode


class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'name']


class StaffProjectSerializer(serializers.ModelSerializer):
    project = ProjectsSerializer()

    class Meta:
        model = StaffProjects
        fields = ['project', 'effort']


class StaffsSerializer(serializers.ModelSerializer):
    efforts = serializers.SerializerMethodField()

    class Meta:
        model = Staffs
        fields = ['id', 'staff_code', 'full_name', 'efforts']

    def get_efforts(self, obj):
        request = self.context['request']
        arr = []
        current_time = request.query_params.get('month')
        if current_time:
            time = convert_string_to_date(current_time)
        else:
            time = datetime.now()
        for tmp in range(-1, 2):
            month = time + relativedelta(months=tmp)
            staffProjects = []
            for item in obj.effort:
                if month.month == item.start_date.month:
                    staffProjects.append(item)

            arr.append({
                "month": month.strftime('%m/%Y'),
                "project_staff": StaffProjectSerializer(staffProjects, many=True).data
            })
        return arr


class StaffsSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Staffs
        fields = ['id', 'staff_code', 'full_name']


class GroupsSerializer(serializers.ModelSerializer):
    staffs = serializers.SerializerMethodField()
    leader = StaffsSerializer1()

    class Meta:
        model = Groups
        fields = ['id', 'name', 'leader', 'staffs']

    def get_staffs(self, obj):
        request = self.context['request']
        return StaffsSerializer(obj.staff, many=True, context={'request': request}).data


class StaffCreateRequestSerializer(serializers.ModelSerializer):
    month = serializers.CharField(required=True)

    class Meta:
        model = StaffProjects
        fields = ['month', 'staff', 'project', 'effort']

    def validate_month(self, value):
        current_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if datetime.strptime(value, '%m/%Y') < current_date:
            raise Exception(ErrorCode.validate_month.value)
        else:
            return value

    def validate(self, data):
        start_date = convert_string_to_date(data['month'])
        instance = StaffProjects.objects.filter(Q(staff_id=data['staff'].id) & ~Q(project_id=data['project'].id)
                                                & Q(start_date__month=start_date.month)
                                                & Q(start_date__year=start_date.year))
        if len(instance) >= 3:
            raise Exception(ErrorCode.number_project.value)
        else:
            efforts = 0
            for obj in instance:
                efforts = efforts + obj.effort
            efforts = efforts + data['effort']
            if efforts <= 0 or efforts > 1:
                raise Exception(ErrorCode.validate_effort.value)
            return data

    def save(self, **kwargs):
        month = self.validated_data["month"]
        staff = self.validated_data["staff"]
        project = self.validated_data["project"]
        start_date = convert_string_to_date(month)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)
        instance = StaffProjects.objects.filter(start_date=start_date, end_date=end_date, staff=staff, project=project)
        if instance.exists():
            instance = instance.first()
            instance.effort = self.validated_data["effort"]
            instance.save()
            return instance
        else:
            instance = StaffProjects.objects.create(
                staff=staff,
                project=project,
                effort=self.validated_data["effort"],
                start_date=start_date,
                end_date=end_date,
            )
            return instance


class StaffCreateResponseSerializer(serializers.ModelSerializer):
    month = serializers.SerializerMethodField()

    class Meta:
        model = StaffProjects
        fields = ['month', 'staff', 'project', 'effort']

    def get_month(self, obj):
        return obj.start_date.strftime('%m/%Y')


class DevelopSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeveloperTypes
        fields = ['id', 'name']


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ranks
        fields = ['id', 'name']


class GroupSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = ['id', 'name']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = ['language_id']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'name']


class StaffSkillSerializer(serializers.ModelSerializer):
    skill = serializers.SerializerMethodField()

    class Meta:
        model = StaffSkills
        fields = ['skill']

    def get_skill(self, obj):
        return SkillSerializer(obj.skill).data


class StaffAllSerializer(serializers.ModelSerializer):
    languages = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    developer_type = DevelopSerializer()
    group = GroupSmallSerializer()
    rank = RankSerializer()

    class Meta:
        model = Staffs
        fields = ['id', 'staff_code', 'full_name', 'working_type_id', 'developer_type', 'rank', 'position_id', 'group',
                  'languages', 'skills']

    def get_languages(self, obj):
        arr = []
        for language in obj.language_set:
            arr.append(language.language_code)
        return arr

    def get_skills(self, obj):
        return StaffSkillSerializer(obj.skill_set, many=True).data


class RequestStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staffs
        fields = ['developer_type', 'rank', 'position_id', 'group', 'working_type_id', 'staff_code', 'full_name', 'note',
                  'experience_from']


class ResponseStaffSerializer(serializers.ModelSerializer):
    developer_type = DevelopSerializer()
    rank = RankSerializer()
    group = GroupSmallSerializer()

    class Meta:
        model = Staffs
        fields = ['id', 'developer_type', 'rank', 'position_id', 'group', 'working_type_id', 'staff_code', 'full_name', 'note',
                  'experience_from']


