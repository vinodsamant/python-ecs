from rest_framework import serializers


class TwitterUpdateSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    user_id = serializers.CharField(required=True)
    post_id = serializers.CharField(required=False)
    access_token = serializers.CharField(required=True)
    provider = serializers.CharField(required=True)
