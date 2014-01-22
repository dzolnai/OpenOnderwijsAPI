from rest_framework import viewsets
from django.utils import timezone
import datetime
import dateutil.tz as tz
import dateutil.parser as parser
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.pagination import CustomPaginationSerializer


from api.models import NewsItem,NewsFeed
from api.serializers import NewsItemSerializer,NewsFeedSerializer

from api.models import Person, Affiliation
from api.serializers import PersonSerializer, PaginatedPersonSerializer, AffiliationSerializer

from api.models import Group, GroupRole
from api.serializers import GroupSerializer, GroupRoleSerializer

from api.models import Building, Room
from api.serializers import BuildingSerializer, RoomSerializer, PaginatedRoomSerializer

from api.models import Lesson, Course
from api.serializers import LessonSerializer, CourseSerializer, PaginatedLessonSerializer

import search

@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'newsfeeds' : reverse('newsfeed-list', request=request, format=format),
		'newsitems' : reverse('newsitem-list', request=request, format=format),
		'persons'   : reverse('person-list', request=request, format=format),
		'groups'    : reverse('group-list', request=request, format=format),
		'grouproles': reverse('grouprole-list', request=request, format=format),
		'affiliations': reverse('affiliation-list', request=request, format=format),
		'buildings' : reverse('building-list', request=request, format=format),
		'rooms'     : reverse('room-list', request=request, format=format),
		'courses'   : reverse('course-list', request=request, format=format),
                'schedule'  : reverse('lesson-list', request=request, format=format),
	})

class NewsItemViewSet(viewsets.ModelViewSet):
	queryset = NewsItem.objects.all()
	serializer_class = NewsItemSerializer
	pagination_serializer_class = CustomPaginationSerializer

class NewsFeedViewSet(viewsets.ModelViewSet):
	queryset = NewsFeed.objects.all()
	serializer_class = NewsFeedSerializer
	pagination_serializer_class = CustomPaginationSerializer


class AffiliationViewSet(viewsets.ModelViewSet):
	queryset = Affiliation.objects.all()
	serializer_class = AffiliationSerializer
	pagination_serializer_class = CustomPaginationSerializer

class PersonViewSet(viewsets.ModelViewSet):
	queryset = Person.objects.all()
	serializer_class = PersonSerializer
	pagination_serializer_class = CustomPaginationSerializer
        def list(self, request):
            query_string = ''
            entries = Person.objects.all()
            # Search 
            if ('q' in request.GET) and request.GET['q'].strip():
                query_string = request.GET['q']
                # you can add additional fields if needed
                entry_query = search.get_query(query_string, ['givenName', 'surName','displayName','mail','telephoneNumber','employeeID','studentID'])
                entries = entries.filter(entry_query)
            # Affiliation filter
            if ('affiliation' in request.GET):
                query_string = request.GET['affiliation']
                entries = entries.filter(affiliations__affiliation=query_string)
            # 5 persons / page
            paginator = Paginator(entries, 5)
            page = request.QUERY_PARAMS.get('page')
            try:
                paged_entries = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                paged_entries = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                paged_entries = paginator.page(paginator.num_pages)
            serializer = PaginatedPersonSerializer(paged_entries, context={'request': request})
            return Response(serializer.data)
 
class PersonMeViewSet(viewsets.ModelViewSet):
	model = Person
        serializer_class = PersonSerializer
        def retrieve(self, request, pk = None):
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
            queryset = Person.objects.get(displayName = userName) #here you could compare to a userName field
            serializer = PersonSerializer(queryset, context={'request': request})
            return Response(serializer.data)
        
class PersonScheduleViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	# Selects only the lessons which are related to the person with the id person_pk
	def list(self, request, person_pk):
            startTime = datetime.datetime.now().replace(hour = 0, minute = 0)
            endTime = start = datetime.datetime.now().replace(hour = 23, minute = 59)
            start = startTime.isoformat()
            end = endTime.isoformat()
            if ('start' in request.GET):
                start = request.QUERY_PARAMS.get('start')
            if ('end' in request.GET):
                end = request.QUERY_PARAMS.get('end')
            start_date = parser.parse(start)
            end_date = parser.parse(end)
            utc = tz.gettz('UTC')
            start_date = start_date.replace(tzinfo=utc)
            end_date = end_date.replace(tzinfo=utc)
            queryset = Lesson.objects.filter(course__groups__members=person_pk, 
            start__gte=start_date, #Date of the lesson should be greater than or equal to begin date of query
            end__lte=end_date) #Date of the lesson should be less than or equal to end date of query
            #every page has 10 lessons
            paginator = Paginator(queryset, 10)
            page = request.QUERY_PARAMS.get('page')
            try:
                lessons = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                lessons = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                lessons = paginator.page(paginator.num_pages)
            serializer = PaginatedLessonSerializer(lessons, context={'request': request})
            return Response(serializer.data)
	
class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	pagination_serializer_class = CustomPaginationSerializer

class GroupScheduleViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	# Selects only the lessons which are related to the group through group_pk
	#If the lesson's course has this group as selected group, then it's taken into account
	def list(self, request, group_pk):
                startTime = datetime.datetime.now().replace(hour = 0, minute = 0)
                endTime = start = datetime.datetime.now().replace(hour = 23, minute = 59)
                start = startTime.isoformat()
                end = endTime.isoformat()
                if ('start' in request.GET):
                    start = request.QUERY_PARAMS.get('start')
                if ('end' in request.GET):
                    end = request.QUERY_PARAMS.get('end')
                start_date = parser.parse(start)
                end_date = parser.parse(end)
                utc = tz.gettz('UTC')
                start_date = start_date.replace(tzinfo=utc)
                end_date = end_date.replace(tzinfo=utc)
		queryset = Lesson.objects.filter(course__groups=group_pk,
                start__gte=start_date, #Date of the lesson should be greater than or equal to begin date of query
                end__lte=end_date) #Date of the lesson should be less than or equal to end date of query)
                #every page has 10 lessons
                paginator = Paginator(queryset, 10)
                page = request.QUERY_PARAMS.get('page')
                try:
                    lessons = paginator.page(page)
                except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                    lessons = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999),
                    # deliver last page of results.
                    lessons = paginator.page(paginator.num_pages)
                serializer = PaginatedLessonSerializer(lessons, context={'request': request})
		return Response(serializer.data)

class GroupRoleViewSet(viewsets.ModelViewSet):
	queryset = GroupRole.objects.all()
	serializer_class = GroupRoleSerializer
	pagination_serializer_class = CustomPaginationSerializer

class BuildingViewSet(viewsets.ModelViewSet):
	queryset = Building.objects.all()
	serializer_class = BuildingSerializer
	pagination_serializer_class = CustomPaginationSerializer

class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	pagination_serializer_class = CustomPaginationSerializer

class BuildingRoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	pagination_serializer_class = CustomPaginationSerializer
        def list(self, request, building_pk):
            queryset = Room.objects.filter(building=building_pk)
            #every page has 5 rooms
            paginator = Paginator(queryset, 5)
            page = request.QUERY_PARAMS.get('page')
            try:
                rooms = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                rooms = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999),
                # deliver last page of results.
                rooms = paginator.page(paginator.num_pages)
            serializer = PaginatedRoomSerializer(rooms, context={'request': request})
            return Response(serializer.data)

class RoomScheduleViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	#Selects only the lessons which are related to the room through room_pk
	def list(self, request, room_pk):
                startTime = datetime.datetime.now().replace(hour = 0, minute = 0)
                endTime = start = datetime.datetime.now().replace(hour = 23, minute = 59)
                start = startTime.isoformat()
                end = endTime.isoformat()
                if ('start' in request.GET):
                    start = request.QUERY_PARAMS.get('start')
                if ('end' in request.GET):
                    end = request.QUERY_PARAMS.get('end')
                start_date = parser.parse(start)
                end_date = parser.parse(end)
                utc = tz.gettz('UTC')
                start_date = start_date.replace(tzinfo=utc)
                end_date = end_date.replace(tzinfo=utc)
                queryset = Lesson.objects.filter(room=room_pk,
                start__gte=start_date, #Date of the lesson should be greater than or equal to begin date of query
                end__lte=end_date) #Date of the lesson should be less than or equal to end date of query
                #every page has 10 lessons
                paginator = Paginator(queryset, 10)
                page = request.QUERY_PARAMS.get('page')
                try:
                    lessons = paginator.page(page)
                except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                    lessons = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999),
                    # deliver last page of results.
                    lessons = paginator.page(paginator.num_pages)
                serializer = PaginatedLessonSerializer(lessons, context={'request': request})
		return Response(serializer.data)
		

class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	pagination_serializer_class = CustomPaginationSerializer
	
class LessonViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	
class CourseScheduleViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	# Selects only the lessons which are related to the course with the id course_pk
	def list(self, request, course_pk):
                startTime = datetime.datetime.now().replace(hour = 0, minute = 0)
                endTime = start = datetime.datetime.now().replace(hour = 23, minute = 59)
                start = startTime.isoformat()
                end = endTime.isoformat()
                if ('start' in request.GET):
                    start = request.QUERY_PARAMS.get('start')
                if ('end' in request.GET):
                    end = request.QUERY_PARAMS.get('end')
                start_date = parser.parse(start)
                end_date = parser.parse(end)
                utc = tz.gettz('UTC')
                start_date = start_date.replace(tzinfo=utc)
                end_date = end_date.replace(tzinfo=utc)
                queryset = Lesson.objects.filter(course=course_pk,
                start__gte=start_date, #Date of the lesson should be greater than or equal to begin date of query
                end__lte=end_date) #Date of the lesson should be less than or equal to end date of query
                #every page has 10 lessons
                paginator = Paginator(queryset, 10)
                page = request.QUERY_PARAMS.get('page')
                try:
                    lessons = paginator.page(page)
                except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                    lessons = paginator.page(1)
                except EmptyPage:
                    # If page is out of range (e.g. 9999),
                    # deliver last page of results.
                    lessons = paginator.page(paginator.num_pages)
                serializer = PaginatedLessonSerializer(lessons, context={'request': request})
		return Response(serializer.data)
		
		
		
		