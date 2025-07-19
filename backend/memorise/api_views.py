from rest_framework.viewsets import ModelViewSet
from .models import Work, Section, Unit
from .serializers import WorkSerializer, SectionSerializer, UnitSerializer

class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class UnitViewSet(ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer