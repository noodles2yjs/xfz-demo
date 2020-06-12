from rest_framework import serializers

from apps.news.models import News, NewsCategory
from apps.xfzauth.serializers import UserSerializer


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')
class NewsSerializer(serializers.ModelSerializer):
    category=NewsCategorySerializer()
    author=UserSerializer()
    class Meta:
        model=News
        fields = ('id', 'title', 'desc', 'thumbnail', 'pub_time', 'category', 'author')

