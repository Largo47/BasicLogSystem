from rest_framework import serializers
from .models import *


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):   # I'm probably only going to need this one
    class Meta:
        model = Log
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
