import django_filters
from api.models import Person


class PersonFilter(django_filters.FilterSet):

    class Meta:
        model = Person
        fields = ['userId', 'surname', 'displayname', 'affiliations', 'gender', 'organization',
                  'department', 'office', 'groups', 'lat', 'lon']