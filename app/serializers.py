from rest_framework import serializers
from .models import Region, Municipality, Entity, Budget, Program


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'slug']

class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ['id', 'name', 'slug']


class RegionsAndMunicipalitiesSerializer(serializers.ModelSerializer):

    municipalities = MunicipalitySerializer(many=True)

    class Meta:
        model = Region
        fields = ['id', 'name', 'municipalities']




class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class EntitySerializer(serializers.ModelSerializer):

    budgets = BudgetSerializer(many=True)

    class Meta:
        model = Entity
        fields = ['id', 'legal_id', 'name', 'slug', 'entity_type_id', 'entity_cat_id', 'budgets']


class MunicipalityAndEntitiesSerializer(serializers.ModelSerializer):
    entities = EntitySerializer(many=True)

    class Meta:
        model = Municipality
        fields = ['id', 'name', 'slug', 'entities']