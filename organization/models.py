from django.db import models
from utils.models import BaseModel
from user.models import Profile


class Group(BaseModel):
    principal_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    level = models.SmallIntegerField()
    group_leader = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING, blank=True, null=True)
    members = models.ManyToManyField('user.Profile', related_name='groups')
    img_file = models.ForeignKey('Image', on_delete=models.DO_NOTHING, related_name='file_group')

    def __str__(self):
        return self.name

    def get_related_leaders(self, visited_groups=[]):
        if self in visited_groups:
            return Profile.objects.filter(role=-1)
        visited_groups.append(self)

        profiles = Profile.objects.filter(role=-1)
        if self.group_leader:
            profiles |= Profile.objects.filter(id=self.group_leader_id)
        if self.principal_group:
            profiles |= self.principal_group.get_related_leaders(visited_groups)
        child_groups = Group.objects.filter(principal_group=self)
        for child_group in child_groups:
            profiles |= child_group.get_related_leaders(visited_groups)
        return profiles

    def get_related_members(self, visited_groups=[]):
        if self in visited_groups:
            return Profile.objects.filter(role=-1)
        visited_groups.append(self)

        profiles = self.members.all()
        if self.group_leader:
            profiles |= Profile.objects.filter(id=self.group_leader_id)
        if self.principal_group:
            profiles |= self.principal_group.get_related_members(visited_groups)
        child_groups = Group.objects.filter(principal_group=self)
        for child_group in child_groups:
            profiles |= child_group.get_related_members(visited_groups)
        return profiles

class Resource(BaseModel):
    name = models.CharField(max_length=50)
    route = models.FileField()
    groups = models.ManyToManyField('Group')

    def __str__(self):
        return self.name

class Image(BaseModel):
    name = models.CharField(max_length=50)
    route = models.FileField(upload_to='images', default='default.png')

    def __str__(self):
        return self.name
