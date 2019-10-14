from rest_framework import routers
from app.viewsets import RegionViewSet, MunicipalityViewSet, EntityViewSet, BudgetViewSet, ProgramViewSet

router = routers.DefaultRouter()
router.register(r'region', RegionViewSet)
router.register(r'municipality', MunicipalityViewSet)
router.register(r'entity', EntityViewSet)
router.register(r'budget', BudgetViewSet)
router.register(r'program', ProgramViewSet)