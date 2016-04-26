from rest_framework import pagination
from rest_framework import serializers


class MetaSerializer(serializers.Serializer):
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')
    totalPages = serializers.Field(source='paginator.num_pages')
    thisPage = serializers.Field(source='number')
    totalItems = serializers.Field(source='paginator.count')
    firstItem = serializers.Field(source='start_index')
    lastItem = serializers.Field(source='end_index')
    version = serializers.Field(source='version')


class CustomPaginationSerializer(pagination.BasePaginationSerializer):
    meta = MetaSerializer(source='*')
    results_field = 'data'
