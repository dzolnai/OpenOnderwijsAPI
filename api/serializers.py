from api.models import Building, Room
from api.models import Course, Minor
from api.models import Group, GroupRole
from api.models import NewsFeed, NewsItem, Schedule
from api.models import Person, Affiliation
from api.models import TestResult
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

""" This mixin adds the primary key always to the result """


class WithPk(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)


# News items

class NewsItemSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    feeds = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pk')
    authors = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = NewsItem
        fields = ('newsitemId', 'feeds', 'publishDate', 'title', 'authors', 'image', 'link', 'content')


# News feeds

class NewsFeedSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    items = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pk')
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='pk')

    class Meta:
        model = NewsFeed
        fields = ('newsfeedId', 'title', 'description', 'items', 'groups', 'lastModified')


# Group roles


class GroupRoleSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    roles = serializers.ListField(child=serializers.CharField())
    group = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    person = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = GroupRole
        fields = ['grouproleId', 'group', 'person', 'roles']


# Groups
class GroupSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['groupId', 'name', 'description', 'type', 'members', 'courses', 'lastModified']


# Persons
class PersonSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    affiliations = serializers.SlugRelatedField(many=True, read_only=True, slug_field='affiliation')
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Person
        fields = ('userId', 'givenname', 'surname', 'displayname', 'commonname', 'nickname', 'affiliations',
                  'mail', 'telephonenumber', 'mobilenumber', 'photoSocial', 'photoOfficial', 'gender',
                  'organization', 'department', 'title', 'office', 'groups', 'lat', 'lon', 'lastModified')


# Buildings
class BuildingSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    completeAddress = serializers.CharField(source='complete_address')

    class Meta:
        model = Building
        fields = ['buildingId', 'abbreviation', 'name', 'description', 'address',
                  'postalCode', 'city', 'lat', 'lon', 'altitude', 'lastModified', 'completeAddress']


# Rooms
class RoomSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    buildingId = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

    class Meta:
        model = Room
        fields = ['roomId', 'buildingId', 'abbreviation', 'name', 'description', 'totalSeats',
                  'totalWorkspaces', 'availableWorkspaces', 'lat', 'lon', 'altitude', 'lastModified']


# Courses
class CourseSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    schedules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['schedules', 'courseId', 'name', 'abbreviation', 'ects', 'description',
                  'goals', 'requirements', 'level', 'format', 'language', 'enrollment',
                  'literature', 'exams', 'schedule', 'groups']


class ScheduleSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    roomId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    courseId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    userId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    groupId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    lecturers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Schedule
        exclude = ['url']


class TestResultsSerializer(WithPk, ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    courseResult = serializers.SerializerMethodField('_courseResult')

    def _courseResult(self, _):
        return self.context['courseResult']

    class Meta:
        model = TestResult
        fields = ['testResultId', 'userId', 'courseId', 'courseResult', 'description',
                  'lastModified', 'assessmentType', 'testDate', 'grade', 'comment', 'passed', 'weight']

# Unused stuff
class MinorSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Minor

# Affiliations
class AffiliationSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    persons = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='person-detail')

    class Meta:
        model = Affiliation
        fields = ('id', 'affiliation', 'persons')