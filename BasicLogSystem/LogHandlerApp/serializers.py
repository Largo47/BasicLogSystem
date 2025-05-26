from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from .models import *


class BaseModelSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    pass


class ProjectSerializer(BaseModelSerializer):
    class Meta:
        model = IssueBin
        fields = '__all__'


class IssueSerializer(BaseModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class OccurrenceSerializer(BaseModelSerializer):
    class Meta:
        model = Occurrence
        fields = '__all__'


class LogSerializer(BaseModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class LogFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogFile
        fields = '__all__'
