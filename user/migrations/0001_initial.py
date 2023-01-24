# Generated by Django 3.2 on 2023-01-24 01:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive'), (2, 'Canceled')], default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('user_creator', models.CharField(max_length=30)),
                ('user_modifier', models.CharField(max_length=30)),
                ('last_action', models.IntegerField(choices=[(0, 'Create'), (1, 'Uptade'), (2, 'Delete')], default=0)),
                ('card_id', models.CharField(max_length=10)),
                ('born_date', models.DateField()),
                ('genre', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], default='F', max_length=1)),
                ('civil_status', models.CharField(choices=[('C', 'Casado'), ('S', 'Soltero')], default='S', max_length=1)),
                ('tel_1', models.CharField(max_length=10)),
                ('tel_2', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('work', models.CharField(max_length=50)),
                ('work_address', models.CharField(max_length=50)),
                ('work_activity', models.CharField(max_length=50)),
                ('work_tel', models.CharField(max_length=10)),
                ('role', models.IntegerField(choices=[(0, 'Administrador'), (1, 'Lider'), (2, 'Miembro')], default=2)),
                ('card_image', models.ImageField(default='profile/document/img/default-card-image.png', upload_to='profile/document/img/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'webp', 'jpeg'])])),
                ('profile_image', models.ImageField(default='profile/img/default-profile-image.png', upload_to='profile/img/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'webp', 'jpeg'])])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HistoricalProfile',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Active'), (1, 'Inactive'), (2, 'Canceled')], default=0)),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('date_modified', models.DateField(blank=True, editable=False)),
                ('user_creator', models.CharField(max_length=30)),
                ('user_modifier', models.CharField(max_length=30)),
                ('last_action', models.IntegerField(choices=[(0, 'Create'), (1, 'Uptade'), (2, 'Delete')], default=0)),
                ('card_id', models.CharField(max_length=10)),
                ('born_date', models.DateField()),
                ('genre', models.CharField(choices=[('F', 'Femenino'), ('M', 'Masculino')], default='F', max_length=1)),
                ('civil_status', models.CharField(choices=[('C', 'Casado'), ('S', 'Soltero')], default='S', max_length=1)),
                ('tel_1', models.CharField(max_length=10)),
                ('tel_2', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('work', models.CharField(max_length=50)),
                ('work_address', models.CharField(max_length=50)),
                ('work_activity', models.CharField(max_length=50)),
                ('work_tel', models.CharField(max_length=10)),
                ('role', models.IntegerField(choices=[(0, 'Administrador'), (1, 'Lider'), (2, 'Miembro')], default=2)),
                ('card_image', models.TextField(default='profile/document/img/default-card-image.png', max_length=100, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'webp', 'jpeg'])])),
                ('profile_image', models.TextField(default='profile/img/default-profile-image.png', max_length=100, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'webp', 'jpeg'])])),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical profile',
                'verbose_name_plural': 'historical profiles',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
