from rest_framework import serializers

from base.messages import ERROR_CODE
from base.utils import validation_error
from base.choices import ROLE_FB, ROLE_TWITTER
from user_contests.models import UserContestsModel
from user_contests.utils import c_facebook, c_twitter
from users.models import User
from users.serializers import UserSocialPostSerializer


class UpdatePostSerializer(UserSocialPostSerializer):
    user = serializers.CharField(required=True)
    fb_feed_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    twitter_feed_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    # provider = serializers.IntegerField()

    class Meta:
        model = UserContestsModel
        fields = UserSocialPostSerializer.Meta.fields + ('user', 'fb_feed_id', 'twitter_feed_id',
                                                         'provider')

    def validate(self, attrs):
        if (attrs['provider'] == ROLE_FB and
                (attrs['fb_id'] is None or
                 not attrs['fb_id'])):
            raise validation_error(ERROR_CODE['4006'])
        if (attrs['provider'] == ROLE_FB and
                (attrs['fb_access_token'] is None or
                 not attrs['fb_access_token'])):
            raise validation_error(ERROR_CODE['4004'])
        if (attrs['provider'] == ROLE_TWITTER and
                (attrs['twitter_access_token'] is None or
                 attrs['twitter_access_token_secret'] is None or
                 not attrs['twitter_access_token'] or
                 not attrs['twitter_access_token_secret'])):
            raise validation_error(ERROR_CODE['4005'])
        return attrs

    def create(self, validated_data):
        # instance = UserContestsModel.objects.filter(user=validated_data['user'])
        # if instance:
        #     fb_feed_id = (validated_data['fb_feed_id']
        #                   if not instance[0].fb_feed_id
        #                   else instance[0].fb_feed_id)
        #     twitter_feed_id = (validated_data['twitter_feed_id']
        #                        if not instance[0].twitter_feed_id
        #                        else instance[0].twitter_feed_id)
        #     fb_access_token = (validated_data['fb_access_token']
        #                        if not instance[0].user.fb_access_token
        #                        else instance[0].user.fb_access_token)
        #     twitter_access_token = (validated_data['twitter_access_token']
        #                             if not instance[0].user.twitter_access_token
        #                             else instance[0].user.twitter_access_token)
        #     twitter_access_token_secret = (validated_data['twitter_access_token_secret']
        #                                    if not instance[0].user.twitter_access_token_secret
        #                                    else instance[0].user.twitter_access_token_secret)
        #     instance.update(fb_feed_id=fb_feed_id,
        #                     twitter_feed_id=twitter_feed_id,
        #                     provider=provider)
        #     User.objects.filter(
        #         id=validated_data['user']).update(
        #         fb_access_token=fb_access_token,
        #         twitter_access_token=twitter_access_token,
        #         twitter_access_token_secret=twitter_access_token_secret)
        # else:
        provider = validated_data['provider']
        user_id = validated_data.pop('user', None)
        fb_access_token = validated_data.pop('fb_access_token', None)
        twitter_access_token = validated_data.pop('twitter_access_token', None)
        twitter_access_token_secret = validated_data.pop('twitter_access_token_secret', None)
        user_obj = User.objects.filter(id=user_id)
        if user_obj:
            user_obj.update(
                fb_access_token=fb_access_token,
                twitter_access_token=twitter_access_token,
                twitter_access_token_secret=twitter_access_token_secret)
            instance = UserContestsModel.objects.create(user=user_obj[0], **validated_data)
            if instance:
                instance.user = user_obj[0]
                instance.save()

            if provider == ROLE_FB:
                fb = c_facebook()
                feed_id = fb.get_latest_post(facebook_id=validated_data['fb_id'],
                                             access_token=fb_access_token)
                likes_count = fb.get_likes_count(feed_id, fb_access_token)
                # comments_count = fb.get_comments_count(feed_id, validated_data['fb_access_token'])
                instance.fb_feed_id = feed_id
                instance.fb_likes_count = likes_count
                instance.save()
            elif provider == ROLE_TWITTER:
                twitter = c_twitter()
                obj_post = twitter.get_post_details(validated_data['twitter_feed_id'])
                instance.twitter_likes_count = obj_post.favorite_count
                instance.save()
            return instance

        raise validation_error(ERROR_CODE['4007'])


class UpdatePostResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContestsModel
        fields = '__all__'


class FacebookLatestPostSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    user_id = serializers.CharField(required=False)
    facebook_id = serializers.CharField(required=True)


class FacebookLikesCountSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = UserContestsModel
        fields = '__all__'


class FBImageToURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContestsModel
        fields = ['fb_image']

    def update(self, instance, validated_data):
        super(FBImageToURLSerializer, self).update(instance, validated_data)
        return instance
