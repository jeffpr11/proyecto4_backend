from datetime import date
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    class State(models.IntegerChoices):
        ACTIVE = 0
        INACTIVE = 1
        CANCELED = 2

    class Log(models.IntegerChoices):
        CREATE = 0
        UPTADE = 1
        DELETE = 2

    state = models.IntegerField(choices=State.choices, default=State.ACTIVE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    user_creator = models.CharField(max_length=30)
    user_modifier = models.CharField(max_length=30)
    last_action = models.IntegerField(choices=Log.choices, default=Log.CREATE)
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
