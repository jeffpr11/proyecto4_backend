from django.db import models
from utils.models import BaseModel


class Event(BaseModel):
    class Type(models.TextChoices):
        ADMISION = 'A'
        REUNION = 'B'
        CONFERENCIA = 'C'

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    type = models.CharField(max_length=1, choices=Type.choices, default=Type.REUNION)
    image = models.ForeignKey('organization.Resource', on_delete=models.DO_NOTHING)
    group = models.ForeignKey('organization.Group', on_delete=models.DO_NOTHING) 
    date_start = models.DateTimeField(auto_now=False)
    date_end = models.DateTimeField(auto_now=False)
    
    def __str__(self):
        return self.name


class Record(BaseModel):
    interested_record = models.BooleanField(default=True)
    confirmed_record = models.BooleanField(default=False)
    event = models.ForeignKey('Event', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.name
    

class Comment(BaseModel):
    content = models.CharField(max_length=100)
    level = models.SmallIntegerField()
    event = models.ForeignKey('Event', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING)
    principal_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return self.name
