""" serializer class for jobs """
# Django Import
from rest_framework import serializers

# Local Django


class RegisterDeviceId(serializers.Serializer):
    """
    used to create and validate register device token
    """
    type = serializers.ChoiceField(choices=["ios", "web"])

    class Meta:
        """
        meta class
        """
        fields = ('registration_id', 'type')

    def update_device_id(self, validated_data, user):
        """
        override this method to create device token for users
        :param user: user data
        :param validated_data:
        :return:
        """
        if validated_data.get('registration_id'):
            user.register_fcm_token(validated_data.get('registration_id'),
                                    validated_data.get('type'))


class RegisterDeviceIdSerializer(RegisterDeviceId):
    """
    This Serializer is used to register device id.
    """
    registration_id = serializers.CharField(max_length=250)
