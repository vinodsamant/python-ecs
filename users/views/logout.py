from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from base.constants import RequestMethod
from base.messages import MESSAGES
from base.permissions import IsAuthenticated
from base.utils import success_response
from users.serializers import LogoutSerializer


class LogoutViewSet(GenericViewSet):
    """

    """

    @action(url_path='logout',
            methods=[RequestMethod.POST],
            detail=False,
            serializer_class=LogoutSerializer,
            permission_class=[IsAuthenticated, ])
    def logout(self, request):
        """

        :param request:
        :return:
        """
        data_serializer = self.serializer_class(data=request.data)
        if data_serializer.is_valid(raise_exception=True):
            data_serializer.save()
            return success_response(MESSAGES[''])
