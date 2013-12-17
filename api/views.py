from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import link

from api.models import NewsItem,NewsFeed
from api.serializers import NewsItemSerializer,NewsFeedSerializer

from api.models import Person, Affiliation
from api.serializers import PersonSerializer, AffiliationSerializer

from api.models import Group, GroupRole
from api.serializers import GroupSerializer, GroupRoleSerializer

from api.models import Building, Room
from api.serializers import BuildingSerializer, RoomSerializer
from api.pagination import CustomPaginationSerializer

@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'newsfeeds': reverse('newsfeed-list', request=request, format=format),
		'newsitems': reverse('newsitem-list', request=request, format=format),
		'persons'  : reverse('person-list', request=request, format=format),
		'groups'   : reverse('group-list', request=request, format=format),
		'buildings' : reverse('building-list', request=request, format=format),
		'rooms'     : reverse('room-list', request=request, format=format),
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

class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	pagination_serializer_class = CustomPaginationSerializer

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
