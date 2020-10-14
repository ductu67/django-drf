from django.db import models
from apps.staff.models import Staffs
from .constants import StatusType, ProjectType

STATUS = (
    (StatusType.CANCELED.value, 'Canceled'),
    (StatusType.COMPLETED.value, 'Completed'),
    (StatusType.INITIALIZING.value, 'Initializing'),
    (StatusType.INPROGRESS.value, 'Inprogress'),
    (StatusType.NOT_STARTED.value, 'Not Started'),
    (StatusType.PENDING.value, 'Pending'),
)

PROJECT_TYPE = (
    (ProjectType.DOMESTIC.value, 'Domestic'),
    (ProjectType.INTERNATIONAL.value, 'International'),
)


class Partners(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'partners'

    def __str__(self):
        return self.name


class Projects(models.Model):
    partner = models.ForeignKey(Partners, on_delete=models.CASCADE, null=True, blank=True)
    project_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    project_type_id = models.IntegerField(choices=PROJECT_TYPE, null=True, blank=True)
    status_id = models.IntegerField(choices=STATUS, null=True, default=StatusType.INITIALIZING.value)
    start_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    end_date = models.DateTimeField(auto_now=False, blank=True, null=True)
    team_leader = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="team_leader_staff", null=True,
                                    blank=True)
    leader = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="leader_staff", null=True, blank=True)
    brse = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="brse_staff", null=True, blank=True)
    comtor = models.ForeignKey(Staffs, on_delete=models.CASCADE, related_name="comtor_staff", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.name


class PlanProjects(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    plan_effort = models.FloatField(blank=True, null=True)
    start_date = models.DateTimeField(auto_now=False, blank=True)
    end_date = models.DateTimeField(auto_now=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'plan_projects'

    def __str__(self):
        return '%s : %s' % (self.project, self.plan_effort)


class StaffProjects(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=False, blank=True)
    end_date = models.DateTimeField(auto_now=False, blank=True)
    effort = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'staff_projects'

    def __str__(self):
        return '%s : %s : %s' % (self.staff, self.project, self.effort)
