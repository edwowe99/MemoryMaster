from rest_framework import serializers
from .models import Work, Section, Unit, UserUnitProgress

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class SectionSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = "__all__"


class WorkSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = "__all__"