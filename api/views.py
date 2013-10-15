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

@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'newsfeeds': reverse('newsfeed-list', request=request, format=format),
		'newsitems': reverse('newsitem-list', request=request, format=format),
	})

class NewsItemViewSet(viewsets.ModelViewSet):
    queryset = NewsItem.objects.all()
    serializer_class = NewsItemSerializer

class NewsFeedViewSet(viewsets.ModelViewSet):
    queryset = NewsFeed.objects.all()
    serializer_class = NewsFeedSerializer