from rest_framework.routers import DefaultRouter
from .api_views import WorkViewSet, SectionViewSet, UnitViewSet

router = DefaultRouter()
router.register(r'works', WorkViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'units', UnitViewSet)

urlpatterns = router.urls