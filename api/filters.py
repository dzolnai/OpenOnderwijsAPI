import django_filters
from api.models import Person, Building, TestResult, Course


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