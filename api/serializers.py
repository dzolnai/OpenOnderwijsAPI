from rest_framework import serializers

from api.models import NewsFeed, NewsItem, Schedule
from api.models import Person, Affiliation
from api.models import Group, GroupRole
from api.models import Building, Room
from api.models import Course, Minor
from api.models import TestResult, CourseResult

from api.pagination import CustomPaginationSerializer

""" This mixin adds the primary key always to the result """
class WithPk(object):
    def get_pk_field(self, model_field):
        return self.get_field(model_field)


# News items


class NewsItemSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    feeds = serializers.HyperlinkedRelatedField(many=True, view_name='newsfeed-detail')

    class Meta:
        model = NewsItem
        fields = ('newsitemId', 'feeds', 'publishDate', 'title', 'authors', 'image', 'link', 'content')


# News feeds


class NewsFeedSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    items = NewsItemSerializer(many=True, read_only=True)

    class Meta:
        model = NewsFeed
        fields = ('newsfeedId', 'title', 'description', 'items', 'groups', 'lastModified')

# Group roles


class GroupRoleSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupRole
        fields = ('grouproleId', 'group', 'person', 'roles')


class GroupRoleSerializerPerson(WithPk, serializers.HyperlinkedModelSerializer):
    group = serializers.HyperlinkedRelatedField(view_name='group-detail', read_only=True)
    groupName = serializers.Field(source='groupName')
    groupType = serializers.Field(source='groupType')

    class Meta:
        model = GroupRole
        fields = ('grouproleId', 'group', 'groupName', 'groupType', 'roles')


class GroupRoleSerializerGroup(WithPk, serializers.HyperlinkedModelSerializer):
    person = serializers.HyperlinkedRelatedField(view_name='person-detail', read_only=True)
    displayName = serializers.Field(source='displayName')
    groupType = serializers.Field(source='groupType')

    class Meta:
        model = GroupRole
        fields = ('grouproleId', 'person', 'displayName', 'groupType', 'roles')


# Groups


class GroupSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    members = GroupRoleSerializerGroup(many=True, read_only=True)
    courses = serializers.HyperlinkedRelatedField(many=True, view_name='course-detail')

    class Meta:
        model = Group
        fields = ('groupId', 'name', 'description', 'type', 'members', 'courses')


# Affiliations


class AffiliationSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    persons = serializers.HyperlinkedRelatedField(many=True, view_name='person-detail')

    class Meta:
        model = Affiliation
        fields = ('id', 'affiliation', 'persons')


# Persons


class PersonSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    affiliations = serializers.SlugRelatedField(many=True, read_only=False, slug_field='affiliation')
    class Meta:
        model = Person
        fields = ('userId', 'givenname', 'surname', 'displayname', 'commonname', 'nickname', 'affiliations',
                  'mail', 'telephonenumber', 'mobilenumber', 'photoSocial', 'photoOfficial', 'gender',
                  'organization', 'department', 'title', 'office', 'groups', 'lat', 'lon', 'lastModified')


class PaginatedPersonSerializer(CustomPaginationSerializer):
    class Meta:
        object_serializer_class = PersonSerializer


# Buildings


class BuildingSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        field = ('abbr', 'name', 'description', 'address', 'postalCode', 'city', 'lat', 'lon')


# Rooms


class RoomSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    building = serializers.HyperlinkedRelatedField(view_name='building-detail')

    class Meta:
        model = Room
        depth = 1
        field = (
        'building', 'abbreviation', 'name', 'description', 'totalSeats', 'totalWorkspaces', 'availableWorkspaces')


class RoomSummarySerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('roomId', 'abbreviation', 'name')


class PaginatedRoomSerializer(CustomPaginationSerializer):
    class Meta:
        object_serializer_class = RoomSerializer


# Courses
class CourseSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    #lessons = serializers.HyperlinkedRelatedField(many=True, view_name='lesson-detail')
    #minors = serializers.HyperlinkedRelatedField(many=True, blank=True, view_name='minor-detail')

    class Meta:
        model = Course
    # field = ('abbr','name','description','address','postalCode','city','lat','lon')


class CourseSummarySerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ('courseId', 'abbreviation', 'name', 'description', 'link')


class MinorSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    #	coourses = serializers.HyperlinkedRelatedField(view_name='course-detail')
    class Meta:
        model = Minor


# Lessons


class ScheduleSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    roomId = serializers.SlugRelatedField(many=True, read_only=False, slug_field='roomId')
    courseId = serializers.SlugRelatedField(many=True, read_only=False, slug_field='courseId')
    userId = serializers.SlugRelatedField(many=True, read_only=False, slug_field='userId')
    groupId = serializers.SlugRelatedField(many=True, read_only=False, slug_field='groupId')
    lecturers = serializers.SlugRelatedField(many=True, read_only=False, slug_field='pk')


    class Meta:
        model = Schedule
        exclude = ['url']


class PaginatedScheduleSerializer(CustomPaginationSerializer):
    class Meta:
        object_serializer_class = ScheduleSerializer


# Results


class TestResultSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    student = serializers.HyperlinkedRelatedField(view_name='person-detail')
    course = serializers.HyperlinkedRelatedField(view_name='course-detail')

    class Meta:
        model = TestResult


class CourseResultSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    student = serializers.HyperlinkedRelatedField(view_name='person-detail')
    course = CourseSerializer(read_only=True)
    testResults = serializers.HyperlinkedRelatedField(many=True, view_name='testresult-detail')

    class Meta:
        model = CourseResult
