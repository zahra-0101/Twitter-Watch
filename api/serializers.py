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
    

class AudienceInfoSerializer(serializers.Serializer):
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    followers_to_following_rate = serializers.IntegerField()
    avg_likeCount = serializers.IntegerField()
    avg_quoteCount = serializers.IntegerField()
    avg_replyCount = serializers.IntegerField()
    audience_sentiment_polarity = serializers.IntegerField()
    audience_sentiment_subjectivity = serializers.IntegerField()
    # user_dic = serializers.JSONField()


class SentimentSerializer(serializers.Serializer):
    followers_count= serializers.IntegerField()
    following_count= serializers.IntegerField()
    verified= serializers.BooleanField()
    viewCount= serializers.IntegerField()
    avg_thread_level= serializers.IntegerField()
    unique_audience_level= serializers.IntegerField()