from rest_framework import serializers


class SearchQuerySerializer(serializers.Serializer):
    q = serializers.CharField(required=True, max_length=200)
    skip = serializers.IntegerField(default=0)
    limit = serializers.IntegerField(default=10, max_value=100)
