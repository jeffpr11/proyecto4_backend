
from django.db import models
from utils.models import BaseModel
from django.core.validators import FileExtensionValidator

from utils.Global import Global


class Group(BaseModel):
    principal_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    level = models.SmallIntegerField()
    group_leader = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING, blank=True, null=True)
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

class Resource(BaseModel):
    
    name = models.CharField(max_length=50)
    route = models.FileField(upload_to = 'resources/', validators = [FileExtensionValidator(allowed_extensions = Global.getFilesAccepted())])
    groups = models.ManyToManyField('Group')
    
    def __str__(self):
        return self.name
 