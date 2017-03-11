from rest_framework import serializers
from login_register.models import ContactMessage

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ('id', 'name', 'email', 'message')
        read_only_fields = ('id',)
