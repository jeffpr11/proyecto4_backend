
from django.db import models
from utils.models import BaseModel
from django.core.validators import FileExtensionValidator

from utils.Global import Global
from user.models import Profile


class Group(BaseModel):
    principal_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    level = models.SmallIntegerField()
    group_leader = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='main_group')
    members = models.ManyToManyField('user.Profile', related_name='members')
    group_image = models.ImageField(
        upload_to='groups/img/', 
        default = 'groups/img/default-group-image.jpg', 
        validators = [
            FileExtensionValidator(
                allowed_extensions = Global.getImageFilesAccepted()
            )
        ])
    
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
    groups = models.ManyToManyField('Group')
    route = models.FileField(
        upload_to = 'resources/', 
        validators = [
            FileExtensionValidator(
                allowed_extensions = Global.getFilesAccepted())
        ])

    def __str__(self):
        return self.name
