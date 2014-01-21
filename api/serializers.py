from rest_framework import serializers

from api.models import NewsFeed, NewsItem
from api.models import Person, Affiliation
from api.models import Group, GroupRole
from api.models import Building, Room
from api.models import Course
from api.models import Lesson

from api.pagination import CustomPaginationSerializer

import logging

""" News items"""
class NewsItemSerializer(serializers.HyperlinkedModelSerializer):
	feeds = serializers.HyperlinkedRelatedField(many=True, view_name='newsfeed-detail')
	class Meta:
		model = NewsItem
		fields = ('id','url','feeds','pubDate','title','author','image','link','content')

""" News feeds """
class NewsFeedSerializer(serializers.HyperlinkedModelSerializer):
	#items = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='newsitem-detail')
	items = NewsItemSerializer(many=True, read_only=True)
	updated = serializers.Field(source='last_updated')
	class Meta:
		model = NewsFeed
		fields = ('id','url','title','description','updated','items')


""" Group roles """
class GroupRoleSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GroupRole
		fields = ('id','group','person','role')

class GroupRoleSerializerPerson(serializers.HyperlinkedModelSerializer):
	group     = serializers.HyperlinkedRelatedField(view_name='group-detail',read_only=True)
	groupName = serializers.Field(source='groupName')
	groupType   = serializers.Field(source='groupType')
	class Meta:
		model = GroupRole
		fields = ('id','group','groupName','groupType','role')

class GroupRoleSerializerGroup(serializers.HyperlinkedModelSerializer):
	person      = serializers.HyperlinkedRelatedField(view_name='person-detail',read_only=True)
	displayName = serializers.Field(source='displayName')
	groupType   = serializers.Field(source='groupType')

	class Meta:
		model = GroupRole
		fields = ('id', 'person','displayName','groupType','role')

		
""" Groups """	
class GroupSerializer(serializers.HyperlinkedModelSerializer):
	members = GroupRoleSerializerGroup(many=True,read_only=True)
	courses = serializers.HyperlinkedRelatedField(many=True, view_name='course-detail')
	class Meta:
		model = Group
		fields = ('id','url','name','description','type','members','courses')


""" Affiliations """
class AffiliationSerializer(serializers.HyperlinkedModelSerializer):
	persons = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail')
	class Meta:
		model = Affiliation
		fields = ('id','affiliation','persons')

""" Persons """
class PersonSerializer(serializers.HyperlinkedModelSerializer):
	affiliations = serializers.SlugRelatedField(many=True, read_only=False, slug_field='affiliation')
	groups = GroupRoleSerializerPerson(many=True,read_only=True)
	class Meta:
		model = Person
		fields = ('id','url','givenName','surName','displayName','affiliations',
			'mail', 'telephoneNumber','mobileNumber','photo','gender',
			'organisation','department','title','office','groups')
                        
""" Buildings """
class BuildingSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Building
		field = ('abbr','name','description','address','postalCode','city','lat','lon')

""" Rooms """
class RoomSerializer(serializers.HyperlinkedModelSerializer):
	building =  serializers.HyperlinkedRelatedField(view_name='building-detail')
	class Meta:
		model = Room
		depth = 1
		field = ('building','abbr','name','description','totalSeats','totalWorkspaces','availableWorkspaces')

""" Lessons """
class LessonSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Lesson
		field = ('id','start','end','course','room','description')		

class PaginatedLessonSerializer(CustomPaginationSerializer):
	class Meta:
            object_serializer_class = LessonSerializer

		
""" Courses """
class CourseSerializer(serializers.HyperlinkedModelSerializer):
	lessons =  serializers.HyperlinkedRelatedField(many=True, view_name='lesson-detail')
	class Meta:
		model = Course
                field = ('abbr', 'name', 'ects', 'description', 'goals', 'requirements', 'level', 'format',
                'language', 'enrollment', 'literature', 'exams', 'schedule', 'url', 'organisation', 'department',
                'lecturers', 'groups')
		
	