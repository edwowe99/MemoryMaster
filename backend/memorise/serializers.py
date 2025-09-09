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


class WorkDetailSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = "__all__"


class WorkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ["id", "slug", "title", "author", "type"]


class UnitPracticeResultSerializer(serializers.Serializer):
    unit_id = serializers.UUIDField()
    score = serializers.FloatField(min_value=0.0, max_value=1.0)
    cap = serializers.FloatField(min_value=0.0, max_value=1.0)


class PracticeResultSerializer(serializers.Serializer):
    work_id = serializers.UUIDField()
    mode = serializers.ChoiceField(choices=["repetition", "practice", "test"])
    units = UnitPracticeResultSerializer(many=True)