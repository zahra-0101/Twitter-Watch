from rest_framework import serializers
from accounts.models import TwitterAccount

class TwitterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterAccount
        fields = '__all__'
