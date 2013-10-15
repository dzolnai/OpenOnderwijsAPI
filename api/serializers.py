from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import NewsFeed, NewsItem

class NewsItemSerializer(serializers.HyperlinkedModelSerializer):
	feeds = serializers.HyperlinkedRelatedField(many=True, view_name='newsfeed-detail')
	class Meta:
		model = NewsItem
		fields = ('url','feeds','pubDate','title','author','image','link','content')


class NewsFeedSerializer(serializers.HyperlinkedModelSerializer):
	#items = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='newsitem-detail')
	items = NewsItemSerializer(many=True, read_only=True)
	updated = serializers.Field(source='last_updated')
	class Meta:
		model = NewsFeed
		fields = ('id','url','title','updated','items')


