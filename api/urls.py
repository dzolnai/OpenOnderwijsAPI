from api.views import BuildingViewSet, RoomViewSet, BuildingRoomViewSet, UserTestResultsViewSet, CourseResultsViewSet
from api.views import CourseViewSet, ScheduleViewSet
from api.views import GroupViewSet, GroupRoleViewSet
from api.views import MinorViewSet
from api.views import NewsFeedViewSet, NewsItemViewSet
from api.views import PersonViewSet, PersonMeViewSet, AffiliationViewSet
from api.views import TestResultViewSet, UserCourseResultsViewSet
from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

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
    'post': 'create',
})

person_list_nearests = PersonViewSet.as_view({
    'get': 'nearests',
})

person_detail = PersonViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

person_me = PersonMeViewSet.as_view({
    'get': 'retrieve',
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

building_list_nearests = BuildingViewSet.as_view({
    'get': 'nearests',
})

building_detail = BuildingViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

building_detail_rooms = BuildingRoomViewSet.as_view({
    'get': 'list',
    'post': 'create'
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

minor_list = MinorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
minor_detail = MinorViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

schedule_list = ScheduleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

schedule_detail = ScheduleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

testresult_list_by_user = UserTestResultsViewSet.as_view({
    'get': 'retrieve'
})
testresult_detail = TestResultViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

courseresult_list_by_user = UserCourseResultsViewSet.as_view({
    'get': 'retrieve',
})
courseresult_detail = CourseResultsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = patterns('api.views',
                       url(r'^$', 'api_root'),

                       url(r'^v1/newsfeeds$', newsfeed_list, name='newsfeed-list'),
                       url(r'^v1/newsfeeds/(?P<pk>[0-9]+)$', newsfeed_detail, name='newsfeed-detail'),
                       url(r'^v1/newsitems$', newsitem_list, name='newsitem-list'),
                       url(r'^v1/newsitems/(?P<pk>[0-9]+)$', newsitem_detail, name='newsitem-detail'),
                       url(r'^v1/persons$', person_list, name='person-list'),
                       url(r'^v1/persons/nearests$', person_list_nearests, name='person-list-nearests'),
                       url(r'^v1/persons/(?P<pk>[0-9]+)$', person_detail, name='person-detail'),
                       url(r'^v1/persons/@me$', person_me, name='person-me'),
                       url(r'^v1/groups$', group_list, name='group-list'),
                       url(r'^v1/groups/(?P<pk>[0-9]+)$', group_detail, name='group-detail'),
                       url(r'^v1/grouproles$', grouprole_list, name='grouprole-list'),
                       url(r'^v1/grouproles/(?P<pk>[0-9]+)$', grouprole_detail, name='grouprole-detail'),
                       url(r'^v1/buildings$', building_list, name='building-list'),
                       url(r'^v1/buildings/nearests$', building_list_nearests, name='building-list-nearests'),
                       url(r'^v1/buildings/(?P<pk>\w+)$', building_detail, name='building-detail'),
                       url(r'^v1/buildings/(?P<building_pk>\w+)/rooms$', building_detail_rooms,
                           name='building-detail-rooms'),
                       url(r'^v1/rooms$', room_list, name='room-list'),
                       url(r'^v1/rooms/(?P<pk>\w+)$', room_detail, name='room-detail'),
                       url(r'^v1/courses$', course_list, name='course-list'),
                       url(r'^v1/courses/(?P<course_id>[\w\-]+)$', course_detail, name='course-detail'),
                       url(r'^v1/schedule$', schedule_list, name='schedule-list'),
                       url(r'^v1/schedule/(?P<pk>[0-9]+)', schedule_detail, name='schedule-detail'),
                       url(r'^v1/testresults/(?P<user_id>[0-9]+)$', testresult_list_by_user,
                           name='testresult-list-by-user'),
                       url(r'^v1/testresults/(?P<user_id>[0-9]+)/(?P<test_id>\w+)$', testresult_detail,
                           name='testresult-detail'),
                       url(r'^v1/courseresults/(?P<user_id>[0-9]+)$', courseresult_list_by_user,
                           name='courseresult-list-by-user'),
                       url(r'^v1/courseresults/(?P<user_id>[0-9]+)/(?P<course_id>[\w\-]+)$', courseresult_detail,
                           name='courseresult-detail'),
                       # Affiliations and minors should not be exposed
                       # url(r'^v1/affiliations$', affiliation_list, name='affiliation-list'),
                       # url(r'^v1/affiliations/(?P<pk>[0-9]+)$', affiliation_detail, name='affiliation-detail'),
                       # url(r'^v1/minors$', minor_list, name='minor-list'),
                       # url(r'^v1/minors/(?P<pk>\w+)$', minor_detail, name='minor-detail'),
                       )

urlpatterns = format_suffix_patterns(urlpatterns)
