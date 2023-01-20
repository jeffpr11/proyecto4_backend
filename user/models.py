
from django.contrib.auth.models import User
from django.db import models
from utils.models import BaseModel


class Profile(BaseModel):
    class Genre(models.TextChoices):
        FEMENINO = 'F'
        MASCULINO = 'M'
    
    class CivilStatus(models.TextChoices):
        CASADO = 'C'
        SOLTERO = 'S'
        
    class Role(models.IntegerChoices):
        ADMINISTRADOR = 0
        LIDER = 1
        MIEMBRO = 2

    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='profile')
    card_id = models.CharField(max_length=10)
    born_date = models.DateField(auto_now=False)
    genre = models.CharField(choices=Genre.choices, default=Genre.FEMENINO, max_length=1)
    civil_status = models.CharField(choices=CivilStatus.choices, default=CivilStatus.SOLTERO, max_length=1)
    tel_1 = models.CharField(max_length=10)
    tel_2 = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    work = models.CharField(max_length=50)
    work_address = models.CharField(max_length=50)
    work_activity = models.CharField(max_length=50)
    work_tel = models.CharField(max_length=10)
    role = models.IntegerField(choices=Role.choices, default=Role.MIEMBRO)
    card_id_file = models.ForeignKey('organization.Image', on_delete=models.DO_NOTHING, related_name='file_id')
    img_file = models.ForeignKey('organization.Image', on_delete=models.DO_NOTHING, related_name='file_avatar')
    
    def __str__(self):
        return self.user.get_full_name()
