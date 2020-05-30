from rest_framework.routers import DefaultRouter

from users.views.login import RegistrationViewSet, LoginViewSet
from users.views.password import VerifyUserByPasswordViewSet
from users.views.profile import UserProfileViewSet

router = DefaultRouter()
router.register(r'registration', RegistrationViewSet, base_name='registration')
router.register(r'login', LoginViewSet, base_name='login')
router.register(r'profile', UserProfileViewSet, base_name='profile')
router.register(r'verify-user-by-password', VerifyUserByPasswordViewSet, base_name='verify-user-by-password')

urlpatterns = router.urls
