from api import filters
from api.filters import TestResultFilter, CourseFilter, ScheduleFilter, RoomFilter, GroupFilter, GroupRoleFilter, \
    NewsFeedFilter, NewsItemFilter
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
from django.db.models import F
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point, D
from oauth2_provider.ext.rest_framework import OAuth2Authentication
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
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
        'buildings': reverse('building-list', request=request, format=format),
        'buildings-nearests': reverse('building-list-nearests', request=request, format=format),
        'rooms': reverse('room-list', request=request, format=format),
        'courses': reverse('course-list', request=request, format=format),
        'schedule': reverse('schedule-list', request=request, format=format),
        # Affiliations and minors should not be exposed
        #'affiliations': reverse('affiliation-list', request=request, format=format),
        #'minors': reverse('minor-list', request=request, format=format),
    })


class AuthenticatedViewSet(viewsets.ModelViewSet):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated]

    def get_user(self, request):
        user = request.user
        username = user.username
        person = Person.objects.filter(displayName=username)
        if len(person) is not 1:
            return None
        else:
            return person[0]




class NewsItemViewSet(AuthenticatedViewSet):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer
    pagination_class = MetadataPagination
    filter_class = NewsItemFilter


class NewsFeedViewSet(AuthenticatedViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer
    pagination_class = MetadataPagination
    filter_class = NewsFeedFilter


class AffiliationViewSet(AuthenticatedViewSet):
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    pagination_class = MetadataPagination


class PersonViewSet(AuthenticatedViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    pagination_class = MetadataPagination
    filter_class = filters.PersonFilter

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


class PersonMeViewSet(AuthenticatedViewSet):
    model = Person
    serializer_class = PersonSerializer

    def retrieve(self, request, pk=None):
        # Use it like this after installing authentication and session middlewares
        current_user = request.user
        # You should create a connection between the django.contrib.auth.User object
        # and between the Person object, for example, by adding a username field to
        # the Person object.
        current_user.username
        # you can check if user is authenticated with:
        #  >>> if request.user.is_authenticated():
        # Now we just test with displayName instead of username        queryset = Person.objects.get(displayname=userName)  # here you could compare to a userName field
        serializer = PersonSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class GroupViewSet(AuthenticatedViewSet):
    lookup_url_kwarg = 'group_id'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = MetadataPagination
    filter_class = GroupFilter


class GroupRoleViewSet(AuthenticatedViewSet):
    lookup_url_kwarg = 'grouprole_id'
    queryset = GroupRole.objects.all()
    serializer_class = GroupRoleSerializer
    pagination_class = MetadataPagination
    filter_class = GroupRoleFilter


class BuildingViewSet(AuthenticatedViewSet):
    queryset = Building.objects.all()
    pagination_class = MetadataPagination
    serializer_class = BuildingSerializer
    filter_class = filters.BuildingFilter

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
    filter_class = RoomFilter


class BuildingRoomViewSet(AuthenticatedViewSet):
    lookup_url_kwarg = 'building_id'
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = MetadataPagination


class CourseViewSet(AuthenticatedViewSet):
    lookup_url_kwarg = 'course_id'
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = MetadataPagination
    filter_class = CourseFilter


class MinorViewSet(AuthenticatedViewSet):
    queryset = Minor.objects.all()
    serializer_class = MinorSerializer
    pagination_class = MetadataPagination


class ScheduleViewSet(AuthenticatedViewSet):
    queryset = Schedule.objects.all().annotate(buildingId=F('roomId__buildingId'))
    serializer_class = ScheduleSerializer
    pagination_class = MetadataPagination
    filter_class = ScheduleFilter


class UserTestResultsViewSet(AuthenticatedViewSet):
    def get_queryset(self):
        return TestResult.objects.filter(userId=self.kwargs['user_id']).order_by('lastModified')

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        last_modified = None
        courses = Course.objects.filter(testResults=queryset)
        if queryset is not None and len(queryset) > 0:
            last_modified = queryset[0].lastModified
        return Response({"testResult.lastModified": last_modified,
                         "courseId": map(lambda course: course.courseId, courses)})


class TestResultViewSet(AuthenticatedViewSet):
    lookup_url_kwarg = 'test_id'
    serializer_class = TestResultsSerializer
    pagination_class = MetadataPagination
    filter_class = TestResultFilter

    def get_queryset(self):
        return TestResult.objects.filter(userId=self.kwargs['user_id'], pk=self.kwargs['test_id'])

    def get_serializer_context(self):
        test_results = self.get_queryset()
        courses = Course.objects.filter(testResults=test_results)
        course_results = CourseResult.objects.filter(student=self.kwargs['user_id'], course=courses)
        course_result_ids = []
        for course_result in course_results:
            course_result_ids.append(course_result.courseResultId)
        return {'courseResult': course_result_ids, 'request': self.request}


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
        course_result = CourseResult.objects.filter(student=self.kwargs['user_id'], course=self.kwargs['course_id'])
        if course_result and len(course_result) == 1:
            self.kwargs['pk'] = course_result[0].pk
        else:
            self.kwargs['pk'] = None
        return queryset

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        course_result = CourseResult.objects.filter(student=self.kwargs['user_id'], course=self.kwargs['course_id'])
        if len(course_result) != 1:
            return super(AuthenticatedViewSet, self).retrieve(self, request, args, kwargs)
        course_result = course_result[0]
        last_modified = None
        if queryset is not None and len(queryset) > 0:
            last_modified = queryset[0].lastModified

        last_modified = max(last_modified, course_result.lastModified)
        grade_sum = 0
        grade_count = 0
        for test_result in queryset:
            if test_result.grade is not None:
                if test_result.weight is not None:
                    weighted_grade = float(test_result.weight) / 100.0 * float(test_result.grade)
                else:
                    weighted_grade = test_result.grade
                grade_sum += weighted_grade
                grade_count += 1
        grade = None if grade_count is 0 else grade_sum / float(grade_count)
        return Response({
            "course": kwargs['course_id'],
            "lastModified": last_modified,
            "testResults": map(lambda test_result_for_user: test_result_for_user.testResultId, queryset),
            "grade": grade,
            "comment": course_result.comment,
            "passed": course_result.passed
        })
