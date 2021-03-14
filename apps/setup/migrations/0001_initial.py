# Generated by Django 2.2.1 on 2021-01-19 19:39

import apps.ke_mixcloud_core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, help_text='This is to make sure deletes are not actual deletes')),
                ('permanent_delete', models.BooleanField(default=False, help_text='This false deletes items from recycle bin')),
                ('name', apps.ke_mixcloud_core.models.UpperCaseField(max_length=255)),
                ('audit_trail_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='role_audit_trail_user', to=settings.AUTH_USER_MODEL)),
                ('createdby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='setup_role_related', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False, help_text='This is to make sure deletes are not actual deletes')),
                ('permanent_delete', models.BooleanField(default=False, help_text='This false deletes items from recycle bin')),
                ('audit_trail_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('createdby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='setup_userrole_related', to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_role_role', to='setup.Role')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_role_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'role')},
            },
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='PermissionMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, help_text='This is to make sure deletes are not actual deletes')),
                ('permanent_delete', models.BooleanField(default=False, help_text='This false deletes items from recycle bin')),
                ('view', models.BooleanField(default=False)),
                ('edit', models.BooleanField(default=False)),
                ('create', models.BooleanField(default=False)),
                ('delete', models.BooleanField(default=False)),
                ('approver', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('audit_trail_user', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissionmap_content_type', to='contenttypes.ContentType')),
                ('createdby', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='setup_permissionmap_related', to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissionmap_role', to='setup.Role')),
            ],
            options={
                'unique_together': {('role', 'content_type')},
            },
            managers=[
                ('everything', django.db.models.manager.Manager()),
            ],
        ),
    ]