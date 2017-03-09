from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from authentication.models import Account

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('id', 'email', 'first_name', 'last_name', 'created_at',
                'updated_at', 'password', 'phone', 'is_courier')
        read_only_fields = ('created_at', 'updated_at')

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)

        return account

    def update(self, instance, validated_data):
        # These would have updated the username if we had them
        #instance.username = validated_data.get('username', instance.username)
        #instance.save()

        password = validated_data.get('password', None)

        instance.set_password(password)
        instance.save()

        return instance
