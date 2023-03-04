from rest_framework import serializers
from accounts.models import TwitterAccount
from accounts.models import TwitterThread


class TwitterAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterAccount
        fields = '__all__'


class TwitterThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterThread
        fields = ['account']

    def to_representation(self, instance):
        queryset = TwitterThread.objects.filter(account__twitter_handle=instance['account'])
        conversations = [thread.conversation for thread in queryset]
        return {'conversations': conversations}