from django.conf.urls import patterns, url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

from api.views import NewsFeedViewSet, NewsItemViewSet
from api.views import PersonViewSet, AffiliationViewSet
from api.views import GroupViewSet, GroupRoleViewSet
from api.views import BuildingViewSet, RoomViewSet
from api.views import PersonScheduleViewSet, GroupScheduleViewSet, RoomScheduleViewSet
from api.views import CourseViewSet, LessonViewSet, CourseLessonViewSet

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

person_list = PersonViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
person_detail = PersonViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
person_detail_schedule = PersonScheduleViewSet.as_view({
	'get': 'list',
})

group_list = GroupViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
group_detail = GroupViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
group_detail_schedule = GroupScheduleViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

grouprole_list = GroupRoleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
grouprole_detail = GroupRoleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

""" affiliations views not enabled by default """ 
affiliation_list = AffiliationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
affiliation_detail = AffiliationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


building_list = BuildingViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
building_detail = BuildingViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

room_list = RoomViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

room_detail = RoomViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
room_detail_schedule = RoomScheduleViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

course_list = CourseViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

course_detail = CourseViewSet.as_view({
	'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

course_detail_lessons = CourseLessonViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

lesson_detail = LessonViewSet.as_view({
	'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = patterns('api.views',
	url( r'^$',                           'api_root'                    ),

	url( r'^newsfeeds$',                   newsfeed_list ,     name='newsfeed-list'     ),
	url( r'^newsfeeds/(?P<pk>[0-9]+)$',    newsfeed_detail,    name='newsfeed-detail'   ),
    url( r'^newsitems$',                   newsitem_list,      name='newsitem-list'     ),
    url( r'^newsitems/(?P<pk>[0-9]+)$',    newsitem_detail,    name='newsitem-detail'   ),

    url( r'^persons$',                     person_list,        name='person-list'       ),
    url( r'^persons/(?P<pk>[0-9]+)$',      person_detail,      name='person-detail'     ),
	url( r'^persons/(?P<person_pk>[0-9]+)/schedule$',	person_detail_schedule,		name='person-detail-schedule'	),
    # affiliations should not be exposed """
    url( r'^affiliations$',                     affiliation_list,        name='affiliation-list'        ),
    url( r'^affiliations/(?P<pk>[0-9]+)$',      affiliation_detail,      name='affiliation-detail'      ),
    url( r'^groups$',                      group_list,         name='group-list'       ),
    url( r'^groups/(?P<pk>[0-9]+)$',       group_detail,       name='group-detail'     ),
	url( r'^groups/(?P<group_pk>[0-9]+)/schedule$',       group_detail_schedule,       name='group-detail-schedule'     ),
    url( r'^grouproles$',                  grouprole_list,     name='grouprole-list'       ),
    url( r'^grouproles/(?P<pk>[0-9]+)$',   grouprole_detail,   name='grouprole-detail'     ),

    url( r'^buildings$',                  building_list,       name='building-list'       ),
    url( r'^buildings/(?P<pk>\w+)$',   building_detail,     name='building-detail'     ),
    url( r'^rooms$',                      room_list,           name='room-list'       ),
    url( r'^rooms/(?P<pk>\w+)$',       room_detail,         name='room-detail'),
	url( r'^rooms/(?P<room_pk>\w+)/schedule$',       room_detail_schedule,         name='room-detail-schedule'     ),
	url( r'^courses/(?P<pk>[0-9]+)$',   course_detail,   name='course-detail'     ),
	url( r'^courses$',   course_list,   name='course-list'     ),
	url( r'^courses/(?P<course_pk>[0-9]+)/lessons$',   course_detail_lessons,   name='course-detail-lessons'     ),
	url( r'^lessons/(?P<pk>[0-9]+)',   lesson_detail,   name='lesson-detail'     ),
)

urlpatterns = format_suffix_patterns(urlpatterns)
