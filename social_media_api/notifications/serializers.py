from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_type', 'target_id', 'timestamp', 'read']
        read_only_fields = ['recipient', 'actor', 'verb', 'target_type', 'target_id', 'timestamp']

    def get_target_type(self, obj):
        if obj.target_content_type:
            return obj.target_content_type.model
        return None

    def get_target_id(self, obj):
        return obj.target_object_id
