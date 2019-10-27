from rest_framework import routers
from app.viewsets import RegionViewSet, MunicipalityViewSet, EntityViewSet, BudgetViewSet, ProgramViewSet

router = routers.DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'municipalities', MunicipalityViewSet)
router.register(r'entities', EntityViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'programs', ProgramViewSet)