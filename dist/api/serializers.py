from rest_framework import serializers

from general.models import Article,Notification,Insight, Event,News,Inspection

class ArticleSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Article
