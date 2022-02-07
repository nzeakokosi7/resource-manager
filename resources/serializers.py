from rest_framework import serializers
from . import models


class ResourceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ResourceLog
        fields = '__all__'
        extra_kwargs = {'id': {'read_only': True}}

    def to_representation(self, data):
        res = super(ResourceLogSerializer, self).to_representation(data)
        data = {'files': res["files"], 'links': res["links"]}
        return {res['datetime']: data}
