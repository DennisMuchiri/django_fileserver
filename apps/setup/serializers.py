from rest_framework import serializers

from apps.setup.models import MyFile
import logging

logger = logging.getLogger(__name__)

class MyFileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    filepath = serializers.FileField(
        max_length=None, allow_empty_file=False)
    uuid = serializers.UUIDField(required=False)
    created_by_uuid = serializers.UUIDField(required=False)
    updated_by_uuid = serializers.UUIDField(required=False)

    class Meta:
        model = MyFile
        fields = ('__all__')
