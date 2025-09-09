from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import WorkViewSet, SectionViewSet, UnitViewSet, PracticeResultView

router = DefaultRouter()
router.register(r'works', WorkViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'units', UnitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('practice-result/', PracticeResultView.as_view(), name="practice-result"),
]