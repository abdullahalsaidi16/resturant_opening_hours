from .models import RestOpening
from rest_framework import serializers

class RestOpeningSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(source='rest_id.name')
    class Meta:
        model = RestOpening
        fields = ['Name']