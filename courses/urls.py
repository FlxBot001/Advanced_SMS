from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, 
    SubjectViewSet,
    StrandViewSet,
    SubStrandViewSet,
    LearningOutcomeViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'strands', StrandViewSet)
router.register(r'sub-strands', SubStrandViewSet)
router.register(r'learning-outcomes', LearningOutcomeViewSet)

urlpatterns = router.urls 