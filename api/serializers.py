from django.forms import widgets
from rest_framework import serializers

from api.models import NewsFeed, NewsItem
from api.models import Person, Affiliation


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
		fields = ('id','url','title','description','updated','items')


""" Person """

class AffiliationSerializer(serializers.HyperlinkedModelSerializer):
	persons = serializers.HyperlinkedRelatedField(many=True, view_name='persons-detail')
	class Meta:
		model = Affiliation
		fields = ('id','affiliation','persons')

class PersonSerializer(serializers.HyperlinkedModelSerializer):
	affiliations = serializers.SlugRelatedField(many=True, read_only=False, slug_field='affiliation')
	class Meta:
		model = Person
		fields = ('id','url','givenName','surName','displayName','affiliations',
			'mail', 'telephoneNumber','mobileNumber','photo','gender',
			'organisation','department','title','office',)


