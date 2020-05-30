from rest_framework import viewsets
from rest_framework.decorators import action

from base.constants import RequestMethod
from base.messages import MESSAGES
from base.permissions import IsAuthenticated
from base.utils import success_response, validation_error
from users.models import UserProfile, User
from users.serializers import UpdateUserProfileSerializer, SocialMediaSyncSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserProfileSerializer
    permission_classes = [IsAuthenticated, ]
    model = User
    http_method_names = [RequestMethod.PUT, RequestMethod.GET,
                         RequestMethod.PATCH]

    def update(self, request, *args, **kwargs):
        """
        This method is used to update the user profile.
        :param request:
        :return:
        """
        instance = User.objects.filter(id=request.user.id).first()
        data_serializer = self.serializer_class(instance, data=request.data,
                                                context={'request': request},
                                                partial=True)
        if data_serializer.is_valid(raise_exception=True):
            data_serializer.update(instance, validated_data=data_serializer.validated_data)
            return success_response(MESSAGES['1003'])
        return validation_error(data_serializer.errors)

    @action(url_path='social-media-sync',
            url_name='social-media-sync',
            methods=[RequestMethod.PATCH],
            detail=False,
            serializer_class=SocialMediaSyncSerializer,
            permission_classes=[IsAuthenticated, ])
    def update_social_media_sync(self, request):
        data_serializer = self.serializer_class(request.user, data=request.data,
                                                context={'request': request},
                                                partial=True)
        if data_serializer.is_valid(raise_exception=True):
            data_serializer.update(request.user, validated_data=request.data)
            return success_response(MESSAGES['1003'])
        return validation_error(data_serializer.errors)
