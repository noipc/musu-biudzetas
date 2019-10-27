from rest_framework import viewsets
from .models import Region, Municipality, Entity, Budget, Program
from .serializers import RegionSerializer, MunicipalitySerializer, RegionsAndMunicipalitiesSerializer, EntitySerializer, MunicipalityAndEntitiesSerializer, BudgetSerializer, ProgramSerializer

class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionsAndMunicipalitiesSerializer

class MunicipalityViewSet(viewsets.ModelViewSet):
    queryset = Municipality.objects.all()
    serializer_class = MunicipalityAndEntitiesSerializer

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer