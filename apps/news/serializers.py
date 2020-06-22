from rest_framework import serializers

from apps.news.models import News, NewsCategory, Comment,Banner
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


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'author', 'pub_time')
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        exclude =('pub_time',)
