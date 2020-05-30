from rest_framework import routers

from .views.social import SocialViewSet

router = routers.DefaultRouter()
router.register(r'social', SocialViewSet, base_name='social')

urlpatterns = router.urls
