from django.db import models

from apps.ke_mixcloud_core.models import AbstractBase, UpperCaseField
from django.contrib.contenttypes.models import ContentType


class PermissionMap(AbstractBase):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     related_name='permissionmap_content_type')
    role = models.ForeignKey('setup.Role', on_delete=models.CASCADE,
                                     related_name='permissionmap_role')
    view = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)
    create = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)
    approver = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.role

    class Meta:
        unique_together = ('role', 'content_type',)



class Role(AbstractBase):
    name = UpperCaseField(max_length=255)


    def __str__(self):
        return self.name


class UserRole(AbstractBase):

    role = models.ForeignKey('setup.Role', on_delete=models.DO_NOTHING,
                         related_name='user_role_role')


    def __str__(self):
        return self.user.first_name + ' ' + self.role.name

    class Meta:
        unique_together = ('user', 'role',)


class Track(AbstractBase):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=5000)
    avi = models.FileField(upload_to='files/tracks/avis', max_length=3000, blank=True, null=True)
    title_avi = models.FileField(upload_to='files/tracks/titleavis', max_length=3000, blank=True, null=True)
    trackfile = models.FileField(upload_to='files/tracks/trackfiles', max_length=3000, blank=True, null=True)
    sample = models.FileField(upload_to='files/tracks/trackfilesamples', max_length=3000, blank=True, null=True)







