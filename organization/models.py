from django.db import models
from utils.models import BaseModel
from django.forms.models import model_to_dict


class Group(BaseModel):
    principal_group = models.ForeignKey('self', on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    level = models.SmallIntegerField()
    group_leader = models.ForeignKey('user.Profile', on_delete=models.DO_NOTHING, blank=True, null=True)
    members = models.ManyToManyField('user.Profile', related_name='members')

    def __str__(self):
        return self.name

    def all_members(self):
        """
            FUNCIONALIDAD PARA LIDERES
            -> miembros de mi grupo

            ESCENARIO 1: Soy lider de grupo principal
            -> lider y miembros de cada sub grupo

            ESCENARIO 2: Soy lider de sub grupo
            -> lider y miembros de grupo principal
        """
        res = {'administradores': [], 'lideres': [], 'miembros': []}
        res['lideres'].append(self.group_leader)
        res['miembros'] += self.members.all()

        qs = Group.objects.filter(principal_group=self)
        for q in qs:
            res['lideres'].append(q.group_leader)
            res['miembros'] += q.members.all()

        if self.principal_group:
            res['lideres'].append(self.principal_group.group_leader)
            res['miembros'] += self.principal_group.members.all()

        res['lideres'] = list(set(res['lideres']))
        res['miembros'] = list(set(res['miembros']))

        # for l in res['lideres']:
        #     if l.user.is_staff:
        #         res['administradores'].append(l)

        res['lideres'] = map(lambda x: model_to_dict(x),
                             list(set(res['lideres'])))
        res['miembros'] = map(lambda x: model_to_dict(x),
                              list(set(res['miembros'])))
        # res['administradores'] = map(lambda x : x.__dict__, list(set(res['administradores'])))
        return res


class Resource(BaseModel):
    name = models.CharField(max_length=50)
    route = models.FileField()
    groups = models.ManyToManyField('Group')

    def __str__(self):
        return self.name
