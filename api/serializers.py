from api.models import Building, Room
from api.models import Course, Minor
from api.models import Group, GroupRole
from api.models import NewsFeed, NewsItem, Schedule
from api.models import Person, Affiliation
from api.models import TestResult, CourseResult
from rest_framework import serializers

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
    class Meta:
        model = GroupRole
        fields = ('grouproleId', 'group', 'person', 'roles')

# Groups


class GroupSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    #members = GroupRoleSerializerGroup(many=True, read_only=True)
    courses = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='course-detail')

    class Meta:
        model = Group
        fields = ('groupId', 'name', 'description', 'type', 'members', 'courses')


# Affiliations


class AffiliationSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    persons = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='person-detail')

    class Meta:
        model = Affiliation
        fields = ('id', 'affiliation', 'persons')


# Persons


class PersonSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    affiliations = serializers.SlugRelatedField(many=True, read_only=True, slug_field='affiliation')
    class Meta:
        model = Person
        fields = ('userId', 'givenname', 'surname', 'displayname', 'commonname', 'nickname', 'affiliations',
                  'mail', 'telephonenumber', 'mobilenumber', 'photoSocial', 'photoOfficial', 'gender',
                  'organization', 'department', 'title', 'office', 'groups', 'lat', 'lon', 'lastModified')



# Buildings


class BuildingSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Building
        fields = ('buildingId', 'abbreviation', 'name', 'description', 'address',
                  'postalCode', 'city', 'lat', 'lon', 'altitude', 'lastModified')


# Rooms


class RoomSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    building = serializers.HyperlinkedRelatedField(read_only=True, view_name='building-detail')

    class Meta:
        model = Room
        depth = 1
        field = (
        'building', 'abbreviation', 'name', 'description', 'totalSeats', 'totalWorkspaces', 'availableWorkspaces')


class RoomSummarySerializer(WithPk, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('roomId', 'abbreviation', 'name')


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
        fields = ['courseId', 'abbreviation', 'name', 'description', 'link']


class MinorSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    #	coourses = serializers.HyperlinkedRelatedField(view_name='course-detail')
    class Meta:
        model = Minor


class ScheduleSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    roomId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    courseId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    userId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    groupId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    lecturers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Schedule
        exclude = ['url']


class TestResultsSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    courseResult = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = TestResult
        fields = ['userId', 'courseId', 'courseResult']


class CourseResultSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    student = serializers.SlugRelatedField(many=False, read_only=True, slug_field='userId')
    course = serializers.SlugRelatedField(many=False, read_only=True, slug_field='courseId')
    #testResults = serializers.SlugRelatedField(many=True, read_only=True, slug_field='testResultId')

    class Meta:
        model = CourseResult
        fields = ['courseResultId', 'student', 'course', 'course_lastModified',
                  'testResults']


class CourseResultListSerializer(WithPk, serializers.HyperlinkedModelSerializer):
    student = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    course = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = CourseResult
        fields = ['courseResultId', 'student', 'course', 'course_lastModified']

