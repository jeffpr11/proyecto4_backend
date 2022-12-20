
from django.db import models
from utils.models import BaseModel


class Group(BaseModel):
    principal_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    level = models.SmallIntegerField()
    group_leader = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING, blank=True, null=True)
    members = models.ManyToManyField('user.Profile', related_name='members')

    def __str__(self):
        return self.name


class Resource(BaseModel):
    name = models.CharField(max_length=50)
    route = models.CharField(max_length=100)
    groups = models.ManyToManyField('Group')
    
    def __str__(self):
        return self.name
 