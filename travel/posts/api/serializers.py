from django.utils.timesince import timesince
from rest_framework import serializers
from posts.models import Post
from accounts.api.serializers import UserDisplaySerializers


class PostModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializers(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'user',
            'title',
            'timestamp',
            'date_display',
            'timesince'
        ]

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d, %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + "ago"
