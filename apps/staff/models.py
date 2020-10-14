from .constants import *
from django.db import models
# from apps.project.models import Groups

WORKINGS = (
    (WorkingType.FULL_TIME.value, 'Full Time'),
    (WorkingType.PART_TIME.value, 'Part Time'),
)

LANGUAGES = (
    (LanguageType.ENGLISH.value, 'English'),
    (LanguageType.JAPANESE.value, 'Japanese'),
    (LanguageType.FRENCH.value, 'French'),
)

POSITIONS = (
    (PositionType.SUB_LEADER_1.value, 'Sub leader 1'),
    (PositionType.SUB_LEADER_2.value, 'Sub_leader_2'),
    (PositionType.LEADER.value, 'Leader'),
    (PositionType.GROUP_LEADER.value, 'Group Leader'),
    (PositionType.MANAGER.value, 'Manager'),
    (PositionType.DIRECTOR.value, 'Director')
)


class DeveloperTypes(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'developer_types'

    def __str__(self):
        return self.name


class Ranks(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'ranks'

    def __str__(self):
        return self.name


class Groups(models.Model):
    name = models.CharField(max_length=255)
    leader = models.ForeignKey('Staffs', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'groups'
        unique_together = ('name', 'leader',)

    def __str__(self):
        return '%s : %s' % (self.name, self.leader)


class Staffs(models.Model):
    developer_type = models.ForeignKey(DeveloperTypes, on_delete=models.CASCADE, null=True, blank=True)
    rank = models.ForeignKey(Ranks, on_delete=models.CASCADE, null=True, blank=True)
    position_id = models.IntegerField(choices=POSITIONS, null=True, blank=True)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, null=True, blank=True)
    working_type_id = models.IntegerField(choices=WORKINGS, null=True, default=WorkingType.FULL_TIME.value)
    staff_code = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    experience_from = models.DateTimeField(blank=True, null=True)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'staffs'

    def __str__(self):
        return self.full_name


class Languages(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=20, choices=LANGUAGES, null=True, default=LanguageType.ENGLISH.value)

    class Meta:
        db_table = 'languages'
        unique_together = ('staff', 'language_code',)

    def __str__(self):
        return '%s : %s' % (self.staff, self.language_code)


class Skills(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'skills'

    def __str__(self):
        return self.name


class StaffSkills(models.Model):
    staff = models.ForeignKey(Staffs, on_delete=models.CASCADE, null=True)
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'staff_skills'
        unique_together = ('staff', 'skill',)

    def __str__(self):
        return '%s : %s' % (self.staff, self.skill)
