import django_filters
from api.models import Person, Building, TestResult, Course, Schedule, Room, Group, GroupRole, NewsFeed, NewsItem


class OrderFilter(django_filters.FilterSet):
    order_by_field = None
    order = django_filters.MethodFilter(action='order_queryset')

    def order_queryset(self, queryset, value):
        ordering = ""  # Ascending
        property_name = value
        if value.endswith("_asc"):
            # Ordering stays the same
            property_name = value[:-4]
        elif value.endswith("_desc"):
            ordering = "-"
            property_name = value[:-5]
        order_by = ordering + property_name
        return queryset.order_by(order_by)


class PersonFilter(OrderFilter):
    class Meta:
        model = Person
        fields = ['userId', 'surname', 'displayname', 'affiliations', 'gender', 'organization',
                  'department', 'office', 'groups', 'lat', 'lon', 'order']


class BuildingFilter(OrderFilter):
    class Meta:
        model = Building
        fields = ['abbreviation', 'name', 'postalCode', 'city', 'lastModified', 'order']


class TestResultFilter(OrderFilter):
    class Meta:
        model = TestResult
        fields = ['courseId', 'passed', 'lastModified', 'order']


class CourseFilter(OrderFilter):
    class Meta:
        model = Course
        fields = ['courseId', 'name', 'lastModified', 'order']


class ScheduleFilter(OrderFilter):

    class Meta:
        model = Schedule
        fields = ['scheduleId', 'roomId', 'courseId', 'startDateTime', 'endDateTime',
                  'groupId', 'lecturers', 'lastModified', 'order']


class RoomFilter(OrderFilter):

    class Meta:
        model = Room
        fields = ['buildingId', 'roomId', 'abbreviation', 'name', 'totalSeats',
                  'totalSeats', 'availableWorkspaces', 'lat', 'lon', 'lastModified', 'order']


class GroupFilter(OrderFilter):

    class Meta:
        model = Group
        fields = ['groupId', 'name', 'type', 'members', 'courses', 'order']


class GroupRoleFilter(OrderFilter):

    class Meta:
        model = GroupRole
        fields = ['grouproleId', 'group', 'person', 'roles', 'order']


class NewsFeedFilter(OrderFilter):

    class Meta:
        model = NewsFeed
        fields = ['newsfeedId', 'title', 'lastModified', 'order']


class NewsItemFilter(OrderFilter):

    class Meta:
        model = NewsItem
        fields = ['newsitemId', 'feeds', 'publishDate', 'authors', 'order']