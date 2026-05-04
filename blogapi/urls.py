from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,BlogViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("", BlogViewSet, basename="blogs")

urlpatterns = router.urls
