from rest_framework import serializers

from base.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    area = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Article
