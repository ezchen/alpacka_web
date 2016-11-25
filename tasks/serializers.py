from rest_framework import serializers
from tasks.models import Task

from authentication.serializers import AccountSerializer

class TaskSerializer(serializers.ModelSerializer):
    # include author model in json response
    author = AccountSerializer(read_only=True, required=False)
    courier = AccountSerializer(read_only=True, required=False)

    class Meta:
        model = Task
        fields = ('id', 'task_heading', 'task_description', 'task_price', 'author',
        'courier', 'pub_date', 'is_completed', 'is_canceled')
        read_only_fields = ('id', 'pub_date')

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(TaskSerializer, self).get_validation_exclusions()
        return exclusions + ['author']
