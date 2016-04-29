import search
from api.models import Building, Room, Schedule, CourseResult
from api.models import Course, Minor
from api.models import Group, GroupRole
from api.models import NewsItem, NewsFeed
from api.models import Person, Affiliation
from api.models import TestResult
from api.pagination import MetadataPagination
from api.serializers import BuildingSerializer, RoomSerializer
from api.serializers import GroupSerializer, GroupRoleSerializer
from api.serializers import MinorSerializer
from api.serializers import NewsItemSerializer, NewsFeedSerializer
from api.serializers import PersonSerializer, AffiliationSerializer
from api.serializers import ScheduleSerializer, CourseSerializer
from api.serializers import TestResultsSerializer
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point, D
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'newsfeeds': reverse('newsfeed-list', request=request, format=format),
        'newsitems': reverse('newsitem-list', request=request, format=format),
        'persons': reverse('person-list', request=request, format=format),
        'persons-nearests': reverse('person-list-nearests', request=request, format=format),
        'groups': reverse('group-list', request=request, format=format),
        'grouproles': reverse('grouprole-list', request=request, format=format),
        'affiliations': reverse('affiliation-list', request=request, format=format),
        'buildings': reverse('building-list', request=request, format=format),
        'buildings-nearests': reverse('building-list-nearests', request=request, format=format),
        'rooms': reverse('room-list', request=request, format=format),
        'courses': reverse('course-list', request=request, format=format),
        'schedule': reverse('schedule-list', request=request, format=format),
        'minors': reverse('minor-list', request=request, format=format),
    })


class AuthenticatedViewSet(viewsets.ModelViewSet):
    # replace the empty braces with the commented line to enable authentication on the whole API
    permission_classes = []  # [permissions.IsAuthenticated]
    # when authentication is enabled: 1. request an access token from /oauth2/access_token
    # 2. include the access token in your request headers: --- Authorization: Bearer YOURTOKEN ---


class NewsItemViewSet(AuthenticatedViewSet):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    pagination_class = MetadataPagination


class NewsFeedViewSet(AuthenticatedViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer
    pagination_class = MetadataPagination


class AffiliationViewSet(AuthenticatedViewSet):
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    pagination_class = MetadataPagination


class PersonViewSet(AuthenticatedViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    pagination_class = MetadataPagination

    def nearests(self, request):
        radius = 200
        if 'lat' in request.GET and 'lon' in request.GET:
            # Order should be lon - lat!
            lon_lat = [float(request.GET['lon']), float(request.GET['lat'])]
            location = Point(lon_lat)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Missing 'lat' and/or 'lon' parameters!")
        if 'r' in request.GET:
            radius = request.GET['r']
        results = SearchQuerySet().models(Person).dwithin('location', location, D(m=radius))
        serializer = PersonSerializer([q.object for q in results], many=True, context={'request': request})
        return Response(serializer.data)

    def list(self, request, **kwargs):
        entries = Person.objects.all()
        # Search
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            # you can add additional fields if needed
            entry_query = search.get_query(query_string,
                                           ['givenname', 'surname', 'displayname', 'mail', 'telephonenumber'])
            self.queryset = entries.filter(entry_query)
        # Affiliation filter
        if 'affiliation' in request.GET:
            query_string = request.GET['affiliation']
            self.queryset = entries.filter(affiliations__affiliation=query_string)
        return super(AuthenticatedViewSet, self).list(self, request, **kwargs)


class PersonMeViewSet(AuthenticatedViewSet):
    model = Person
    serializer_class = PersonSerializer

    def retrieve(self, request, pk=None):
        # Use it like this after installing authentication and session middlewares
        #  >>> current_user = request.user
        # You should create a connection between the django.contrib.auth.User object
        # and between the Person object, for example, by adding a username field to
        # the Person object.
        #  >>> username = current_user.username
        # you can check if user is authenticated with:
        #  >>> if request.user.is_authenticated():
        # Now we just test with displayName instead of username
        userName = "Dr. Bibber"
        queryset = Person.objects.get(displayname=userName)  # here you could compare to a userName field
        serializer = PersonSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class GroupViewSet(AuthenticatedViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MetadataPagination


class GroupRoleViewSet(AuthenticatedViewSet):
    queryset = GroupRole.objects.all()
    serializer_class = GroupRoleSerializer
    pagination_class = MetadataPagination


class BuildingViewSet(AuthenticatedViewSet):
    queryset = Building.objects.all()
    pagination_class = MetadataPagination
    serializer_class = BuildingSerializer

    def nearests(self, request):
        radius = 200
        if 'lat' in request.GET and 'lon' in request.GET:
            # Order should be lon - lat!
            lon_lat = [float(request.GET['lon']), float(request.GET['lat'])]
            location = Point(lon_lat)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Missing 'lat' and/or 'lon' parameters!")
        if 'r' in request.GET:
            radius = request.GET['r']
        results = SearchQuerySet().models(Building).dwithin('location', location, D(m=radius))
        serializer = BuildingSerializer([q.object for q in results], many=True, context={'request': request})
        return Response(serializer.data)


class RoomViewSet(AuthenticatedViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = MetadataPagination


class BuildingRoomViewSet(AuthenticatedViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = MetadataPagination


class CourseViewSet(AuthenticatedViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MetadataPagination


class MinorViewSet(AuthenticatedViewSet):
    queryset = Minor.objects.all()
    serializer_class = MinorSerializer
    pagination_class = MetadataPagination


class ScheduleViewSet(AuthenticatedViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    pagination_class = MetadataPagination


class UserTestResultsViewSet(AuthenticatedViewSet):
    def get_queryset(self):
        return TestResult.objects.filter(userId=self.kwargs['pk']).order_by('lastModified')

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        last_modified = None
        courses = []
        if queryset != None and len(queryset) > 0:
            last_modified = queryset[0].lastModified
            for testResult in queryset:
                courses.append(testResult.courseId)
        return Response({"testResult.lastModified": last_modified,
                         "courseId": courses})


class TestResultViewSet(AuthenticatedViewSet):
    serializer_class = TestResultsSerializer
    pagination_class = MetadataPagination

    def get_queryset(self):
        return TestResult.objects.filter(userId=self.kwargs['user_id'], pk=self.kwargs['pk'])


class UserCourseResultsViewSet(AuthenticatedViewSet):
    serializer_class = TestResultsSerializer
    pagination_class = MetadataPagination

    def get_queryset(self):
        return TestResult.objects.filter(userId=self.kwargs['user_id']).order_by('lastModified')

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        last_modified = None
        courses = Course.objects.filter(testResults=queryset)
        course_ids = set(map(lambda course: course.courseId, courses))
        if queryset is not None and len(queryset) > 0:
            last_modified = queryset[0].lastModified
        return Response({
            "student": kwargs['user_id'],
            "course.lastModified": last_modified,
            "course": course_ids
        })


class CourseResultsViewSet(AuthenticatedViewSet):
    serializer_class = TestResultsSerializer
    pagination_class = MetadataPagination

    def get_queryset(self):
        queryset = TestResult.objects.filter(userId=self.kwargs['user_id'], courseId=self.kwargs['course_id'])
        course_result = CourseResult.objects.filter(userId=self.kwargs['user_id'], courseId=self.kwargs['course_id'])
        if course_result:
            self.kwargs['pk'] = course_result.pk
        else:
            self.kwargs['pk'] = None
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_result = CourseResult.objects.filter(userId=self.kwargs['user_id'], courseId=self.kwargs['course_id'])
        last_modified = None
        if queryset is not None and len(queryset) > 0:
            last_modified = queryset[0].lastModified
        last_modified = max(last_modified, course_result.lastModified)
        grade_sum = 0
        grade_count = 0
        for test_result in queryset:
            if test_result.grade is not None:
                grade_sum += test_result.grade
                grade_count += 1
        grade = None if grade_count is 0 else grade_sum / float(grade_count)
        return Response({
            "course": kwargs['course_id'],
            "lastModified": last_modified,
            "testResults": map(lambda test_result: test_result.testResultId, queryset),
            "grade": grade,
            "comment": course_result.comment,
            "passed": course_result.passed
        })
