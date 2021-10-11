from rest_framework import serializers
from .models import *

class RawDataSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # and here you change the default behavior of the serializer
        return RawData(**validated_data)

    class Meta:
        model = RawData
        fields = '__all__'

