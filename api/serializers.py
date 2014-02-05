from rest_framework import serializers

from api.models import NewsFeed, NewsItem
from api.models import Person, Affiliation
from api.models import Group, GroupRole
from api.models import Building, Room
from api.models import Course, Minor
from api.models import Lesson
from api.models import TestResult, CourseResult

from api.pagination import CustomPaginationSerializer

import logging

""" This mixin adds the primary key always to the result """
class WithPk(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)
    
""" News items"""
class NewsItemSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	feeds = serializers.HyperlinkedRelatedField(many=True, view_name='newsfeed-detail')
	class Meta:
		model = NewsItem
		fields = ('id','url','feeds','pubDate','title','author','image','link','content')

""" News feeds """
class NewsFeedSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	#items = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='newsitem-detail')
	items = NewsItemSerializer(many=True, read_only=True)
	updated = serializers.Field(source='last_updated')
	class Meta:
		model = NewsFeed
		fields = ('id','url','title','description','updated','items')


""" Group roles """
class GroupRoleSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	class Meta:
		model = GroupRole
		fields = ('id','group','person','role')

class GroupRoleSerializerPerson(WithPk, serializers.HyperlinkedModelSerializer):
	group     = serializers.HyperlinkedRelatedField(view_name='group-detail',read_only=True)
	groupName = serializers.Field(source='groupName')
	groupType   = serializers.Field(source='groupType')
	class Meta:
		model = GroupRole
		fields = ('id','group','groupName','groupType','role')

class GroupRoleSerializerGroup(WithPk, serializers.HyperlinkedModelSerializer):
	person      = serializers.HyperlinkedRelatedField(view_name='person-detail',read_only=True)
	displayName = serializers.Field(source='displayName')
	groupType   = serializers.Field(source='groupType')

	class Meta:
		model = GroupRole
		fields = ('id', 'person','displayName','groupType','role')

		
""" Groups """	
class GroupSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	members = GroupRoleSerializerGroup(many=True,read_only=True)
	courses = serializers.HyperlinkedRelatedField(many=True, view_name='course-detail')
	class Meta:
		model = Group
		fields = ('id','url','name','description','type','members','courses')


""" Affiliations """
class AffiliationSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	persons = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail')
	class Meta:
		model = Affiliation
		fields = ('id','affiliation','persons')

""" Persons """
class PersonSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	affiliations = serializers.SlugRelatedField(many=True, read_only=False, slug_field='affiliation')
	groups = GroupRoleSerializerPerson(many=True,read_only=True)
	class Meta:
		model = Person
		fields = ('id','url','givenName','surName','displayName','affiliations',
			'mail', 'telephoneNumber','mobileNumber','photo','gender',
			'organisation','department','title','office','groups')

class PaginatedPersonSerializer(CustomPaginationSerializer):
	class Meta:
            object_serializer_class = PersonSerializer
            
""" Buildings """
class BuildingSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Building
		field = ('abbr','name','description','address','postalCode','city','lat','lon')

""" Rooms """
class RoomSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	building =  serializers.HyperlinkedRelatedField(view_name='building-detail')
	class Meta:
		model = Room
		depth = 1
		field = ('building','abbr','name','description','totalSeats','totalWorkspaces','availableWorkspaces')
                
class PaginatedRoomSerializer(CustomPaginationSerializer):
	class Meta:
            object_serializer_class = RoomSerializer

""" Courses """
class CourseSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	lessons = serializers.HyperlinkedRelatedField(many=True, view_name='lesson-detail')
	minors  = serializers.HyperlinkedRelatedField(many=True, blank=True, view_name='minor-detail')
	class Meta:
		model = Course
		#field = ('abbr','name','description','address','postalCode','city','lat','lon')

class MinorSerializer(WithPk, serializers.HyperlinkedModelSerializer):
#	coourses = serializers.HyperlinkedRelatedField(view_name='course-detail')
	class Meta:
		model = Minor

""" Lessons """
class LessonSerializer(WithPk, serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Lesson
		field = ('id','start','end','course','room','description')		

class PaginatedLessonSerializer(CustomPaginationSerializer):
	class Meta:
            object_serializer_class = LessonSerializer


""" Results """

class TestResultSerializer(WithPk, serializers.HyperlinkedModelSerializer):
        student = serializers.HyperlinkedRelatedField(view_name='person-detail')
        course  = serializers.HyperlinkedRelatedField(view_name='course-detail')
        class Meta:
                model = TestResult

class CourseResultSerializer(WithPk, serializers.HyperlinkedModelSerializer):
        student     = serializers.HyperlinkedRelatedField(view_name='person-detail')
        course      = serializers.HyperlinkedRelatedField(view_name='course-detail')
        testResults = serializers.HyperlinkedRelatedField(many=True,view_name='testresult-detail')
        class Meta:
                model = CourseResult