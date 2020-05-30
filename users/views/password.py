from rest_framework import viewsets

from base.constants import RequestMethod
from base.messages import MESSAGES
from base.permissions import IsAuthenticated
from base.utils import success_response, validation_error
from users.models import User
from users.serializers import VerifyUserByPasswordSerializer


class VerifyUserByPasswordViewSet(viewsets.ModelViewSet):

    model = User
    queryset = User.objects.all()
    serializer_class = VerifyUserByPasswordSerializer
    permission_classes = [IsAuthenticated, ]
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        data = self.serializer_class(data=request.data,
                                     context={'request': request.user})
        if data.is_valid(raise_exception=True):
            return success_response(MESSAGES['1004'])
        return validation_error(data.errors)
