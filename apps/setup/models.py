from django.db import models
import uuid

from apps.ke_mixcloud_core.models import AbstractBase, UpperCaseField


class MyFile(AbstractBase):
    name = models.CharField(max_length=300, blank=False, null=False)
    description = models.CharField(max_length=5000, blank=True, null=True)
    filepath = models.FileField(upload_to='files/myfile/', max_length=15000, blank=True, null=True)
    uuid = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, blank=False, null=False)
    created_by_uuid = models.UUIDField(editable=False, unique=False, blank=True, null=True)
    updated_by_uuid = models.UUIDField(editable=False, unique=False, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'my_file'