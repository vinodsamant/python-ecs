from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from base.constants import RequestMethod
from base.messages import MESSAGES
from base.utils import success_response, validation_error
from users.models import User
from users.serializers import RegistrationSerializer, LoginSerializer


class RegistrationViewSet(viewsets.ModelViewSet):

    model = User
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = [RequestMethod.POST]
    permission_classes = []

    def create(self, request, *args, **kwargs):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()
            return success_response(MESSAGES['1001'])
        return validation_error(user_serializer.errors)


class LoginViewSet(viewsets.ModelViewSet):

    model = User
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    http_method_names = [RequestMethod.POST]
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # user_obj = serializer.save()
            # user = LoginResponseSerializer(user_obj).data
            return success_response(serializer.validated_data)
        return validation_error(serializer.errors)
