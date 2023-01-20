# Generated by Django 3.2 on 2023-01-20 12:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_profile_card_id_resource'),
        ('organization', '0004_auto_20230115_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive'), (2, 'Canceled')], default=0)),
                ('date_created', models.DateField(default=datetime.date.today, null=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('user_creator', models.CharField(max_length=30)),
                ('user_modifier', models.CharField(max_length=30)),
                ('last_action', models.IntegerField(choices=[(0, 'Create'), (1, 'Uptade'), (2, 'Delete')], default=0)),
                ('name', models.CharField(max_length=50)),
                ('route', models.FileField(default='default.png', upload_to='images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups', to='user.Profile'),
        ),
    ]
