from rest_framework import serializers

from apps.setup.models import MyFile


class MyFileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    filepath = serializers.CharField(required=True)
    updated_by = serializers.CharField(required=False)
    uuid = serializers.UUIDField(required=True)
    created_by_uuid = serializers.UUIDField(required=True)
    updated_by_uuid = serializers.UUIDField(required=False)

    class Meta:
        model = MyFile
        fields = ('__all__')
