from django.contrib.auth import get_user_model
from rest_framework import serializers

MyUser = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id_author = serializers.IntegerField(source='id')

    class Meta:
        model = MyUser
        fields = ("id_author", "username", "password", "status")

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user


class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'status')
