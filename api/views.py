from rest_framework import viewsets
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.pagination import CustomPaginationSerializer


from api.models import NewsItem,NewsFeed
from api.serializers import NewsItemSerializer,NewsFeedSerializer

from api.models import Person, Affiliation
from api.serializers import PersonSerializer, AffiliationSerializer

from api.models import Group, GroupRole
from api.serializers import GroupSerializer, GroupRoleSerializer

from api.models import Building, Room
from api.serializers import BuildingSerializer, RoomSerializer

from api.models import Lesson, Course
from api.serializers import LessonSerializer, CourseSerializer, PaginatedLessonSerializer

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
		'courses'	: reverse('course-list', request=request, format=format),
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

class PersonScheduleViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	# Selects only the lessons which are related to the person with the id person_pk
	def list(self, request, person_pk):
            #Example date: 201401211206UTC = 2014.01.21 12:06 UTC timezone (you can use, EST, CET, etc.)
            start = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%Z")
            end = start
            if ('start' in request.GET):
                start = request.QUERY_PARAMS.get('start')
            if ('end' in request.GET):
                end = request.QUERY_PARAMS.get('end')
            start_date = datetime.datetime.strptime(start, "%Y%m%d%H%M%Z")
            end_date = datetime.datetime.strptime(end, "%Y%m%d%H%M%Z")
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
                #Example date: 201401211206UTC = 2014.01.21 12:06 UTC timezone (you can use, EST, CET, etc.)
                start = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%Z")
                end = start
                if ('start' in request.GET):
                    start = request.QUERY_PARAMS.get('start')
                if ('end' in request.GET):
                    end = request.QUERY_PARAMS.get('end')
                start_date = datetime.datetime.strptime(start, "%Y%m%d%H%M%Z")
                end_date = datetime.datetime.strptime(end, "%Y%m%d%H%M%Z")
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

class RoomScheduleViewSet(viewsets.ModelViewSet):
	queryset = Lesson.objects.all()
	serializer_class = LessonSerializer
	pagination_serializer_class = CustomPaginationSerializer
	#Selects only the lessons which are related to the room through room_pk
	def list(self, request, room_pk):
                #Example date: 201401211206UTC = 2014.01.21 12:06 UTC timezone (you can use, EST, CET, etc.)
		start = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%Z")
                end = start
                if ('start' in request.GET):
                    start = request.QUERY_PARAMS.get('start')
                if ('end' in request.GET):
                    end = request.QUERY_PARAMS.get('end')
                start_date = datetime.datetime.strptime(start, "%Y%m%d%H%M%Z")
                end_date = datetime.datetime.strptime(end, "%Y%m%d%H%M%Z")
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
		queryset = Lesson.objects.filter(course=course_pk)
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
		
		
		
		