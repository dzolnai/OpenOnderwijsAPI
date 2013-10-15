from django.conf.urls import patterns, url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from api.views import NewsFeedViewSet, NewsItemViewSet


newsfeed_list = NewsFeedViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
newsfeed_detail = NewsFeedViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

newsitem_list = NewsItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
newsitem_detail = NewsItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = patterns('api.views',
	url( r'^$',                           'api_root'                    ),
	url( r'^newsfeeds$',                   newsfeed_list ,     name='newsfeed-list'     ),
	url( r'^newsfeeds/(?P<pk>[0-9]+)$',    newsfeed_detail,    name='newsfeed-detail'   ),
	url( r'^newsitems$',                   newsitem_list,      name='newsitem-list'        ),
	url( r'^newsitems/(?P<pk>[0-9]+)$',    newsitem_detail,    name='newsitem-detail'      ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
