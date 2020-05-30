# Django imports
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# local imports
from base.constants import RequestMethod
from base.permissions import IsAuthenticated
from user_contests.serializers.s_facebook import (UpdatePostSerializer, FacebookLatestPostSerializer,
                                                  UpdatePostResponseSerializer, FBImageToURLSerializer)
from user_contests.utils import c_facebook


class SocialViewSet(GenericViewSet):
    """
    This viewset is used to handle social media
    operations like post on wall, fetch likes and comments counts.
    """

    @action(methods=['post'], detail=False,
            url_path='update_post',
            serializer_class=UpdatePostSerializer,
            permission_classes=[IsAuthenticated, ]
            )
    def update_post(self, request):
        """
        **DESCRIPTION**:
        This method is used to save basic info of ``FB`` and ``Twitter``. After posting on FB/twitter wall this method
        will be called to fetch latest post and likes.


    **REQUEST BODY**:

    .. code-block:: http

        GET  /user_contests/social/update_post/


    .. code-block:: json

        Value of provider = 1: 'fb',
                            2: 'twitter'

        {
          "fb_id": "string",
          "twitter_id": "string",
          "fb_access_token": "string",
          "twitter_access_token": "string",
          "twitter_access_token_secret": "string",
          "user": "string",
          "fb_feed_id": "string",
          "twitter_feed_id": "string",
          "provider": 1
        }

    **RESPONSE BODY**:

    .. code-block:: return

        - 200: Post Data saved successfully.
        - 403: Unauthorized.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            update_response = UpdatePostResponseSerializer(post)

            return Response({'details': update_response.data}, status=status.HTTP_200_OK)
        return Response({'details': serializer.errors}, status=status.HTTP_200_OK)

    @action(methods=[RequestMethod.PUT], detail=False,
            url_path='fb-image-to-url',
            serializer_class=FBImageToURLSerializer,
            permission_classes=[IsAuthenticated, ]
            )
    def fb_image_to_url(self, request):
        """
        **DESCRIPTION**:
        This method is used to upload ``FB`` image and convert into URL.


    **REQUEST BODY**:

    .. code-block:: http

        GET  /user_contests/social/fb-image-to-url/


    .. code-block:: json


        {
          "fb_id": "string",
          "twitter_id": "string",
          "fb_access_token": "string",
          "twitter_access_token": "string",
          "twitter_access_token_secret": "string",
          "user": "string",
          "fb_feed_id": "string",
          "twitter_feed_id": "string",
          "provider": 1
        }

    **RESPONSE BODY**:

    .. code-block:: return

        - 200: Post Data saved successfully.
        - 403: Unauthorized.
        """
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            update_response = UpdatePostResponseSerializer(post)

            return Response({'details': update_response.data}, status=status.HTTP_200_OK)
        return Response({'details': serializer.errors}, status=status.HTTP_200_OK)

    # @action(methods=['get'], detail=False,
    #         url_path='get_latest_post',
    #         serializer_class=FacebookLatestPostSerializer)
    # def get_latest_post(self, request):
    #     """
    #     **DESCRIPTION**:
    # ``GET`` details of the latest post from facebook wall on the basis of ``Facebook ID``.
    # This method will give the post id and on the basis of ID, likes and comments will be fetched.
    #
    #
    #  **REQUEST BODY**:
    #
    # .. code-block:: http
    #
    #     GET  /user_contests/social/get_latest_post/
    #
    #
    # **RESPONSE BODY**:
    #
    # .. code-block:: return
    #
    #     - 200: Fetch total likes count of posted feed on wall.
    #     - 403: Unauthorized.
    #   """
    #     fb = c_facebook()
    #     latest_post = fb.get_latest_post(facebook_id=request.query_params['facebook_id'])
    #     return Response({'likes_count': latest_post}, status=status.HTTP_200_OK)
    #
    # @action(methods=['get'], detail=False,
    #         url_path='get_likes_count')
    # def get_likes_count(self, request):
    #     """
    #     **DESCRIPTION**:
    #     ``GET`` the latest post total likes count on the basis of ``Facebook Feed ID``. This will be updated in the DB
    #  and then used in the contests.
    #
    #
    # **REQUEST BODY**:
    #
    # .. code-block:: http
    #
    #     GET  /user_contests/social/get_likes_count/
    #
    #
    # **RESPONSE BODY**:
    #
    # .. code-block:: return
    #
    #     - 200: Fetch total likes count of posted feed on wall.
    #     - 403: Unauthorized.
    #     """
    #     fb = c_facebook()
    #     count = fb.get_likes_count('103821291152560_105935810941108')
    #     return Response({'likes_count': count}, status=status.HTTP_200_OK)
    #
    # @action(methods=['get'], detail=False,
    #         url_path='get_comments_count')
    # def get_comments_count(self, request):
    #     """
    #     **DESCRIPTION**:
    # ``GET`` the latest post total comments count on the basis of ``Facebook Feed ID``. This will be updated in the DB
    #  and then used in the contests.
    #
    #
    # **REQUEST BODY**:
    #
    # .. code-block:: http
    #
    #     GET  /user_contests/social/get_comments_count/
    #
    #
    # **RESPONSE BODY**:
    #
    # .. code-block:: return
    #
    #     - 200: Fetch total comments count of posted feed on wall.
    #     - 403: Unauthorized.
    #     """
    #     fb = c_facebook()
    #     count = fb.get_comments_count('103821291152560_105935810941108')
    #     return Response({'comments_count': count}, status=status.HTTP_200_OK)
