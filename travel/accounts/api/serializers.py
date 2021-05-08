from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

User = get_user_model()


class UserDisplaySerializers(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "username",
            "follower_count",
            "url",
        ]

    def get_follower_count(self, obj):
        return 0

    def get_url(self, obj):
        return reverse_lazy(
            "accounts:detail", kwargs={"username": obj.username}
        )


