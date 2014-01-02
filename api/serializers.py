from django.forms import widgets
from rest_framework import serializers

from api.models import NewsFeed, NewsItem
from api.models import Person, Affiliation
from api.models import Group, GroupRole
from api.models import Building, Room

import logging

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


""" GroupsRole """
class GroupRoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GroupRole
		fields = ('group','person','role')

class GroupRoleSerializerPerson(serializers.HyperlinkedModelSerializer):
	group     = serializers.HyperlinkedRelatedField(view_name='group-detail',read_only=True)
	groupName = serializers.Field(source='groupName')
	groupType   = serializers.Field(source='groupType')
	class Meta:
		model = GroupRole
		fields = ('group','groupName','groupType','role')

class GroupRoleSerializerGroup(serializers.HyperlinkedModelSerializer):
	person      = serializers.HyperlinkedRelatedField(view_name='person-detail',read_only=True)
	displayName = serializers.Field(source='displayName')
	groupType   = serializers.Field(source='groupType')

	class Meta:
		model = GroupRole
		fields = ('person','displayName','groupType','role')



""" Group """

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	members = GroupRoleSerializerGroup(many=True,read_only=True)
	class Meta:
		model = Group
		fields = ('id','url','name','description','type','members')



""" Person """

class AffiliationSerializer(serializers.HyperlinkedModelSerializer):
	persons = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail')
	class Meta:
		model = Affiliation
		fields = ('id','affiliation','persons')


class PersonSerializer(serializers.HyperlinkedModelSerializer):
	affiliations = serializers.SlugRelatedField(many=True, read_only=False, slug_field='affiliation')
	groups = GroupRoleSerializerPerson(many=True,read_only=True)

	class Meta:
		model = Person
		fields = ('id','url','givenName','surName','displayName','affiliations',
			'mail', 'telephoneNumber','mobileNumber','photo','gender',
			'organisation','department','title','office','groups')


""" Rooms """

class BuildingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Building
		field = ('abbr','name','description','address','postalCode','city','lat','lon')

class RoomSerializer(serializers.HyperlinkedModelSerializer):
	building =  serializers.HyperlinkedRelatedField(view_name='building-detail')
#	building =  BuildingSerializer()
	class Meta:
		model = Room
		depth = 1
		field = ('building','abbr','name','description','totalSeats','totalWorkspaces','availableWorkspaces')

