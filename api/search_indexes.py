from haystack import indexes
from api.models import Person
from api.models import Building

class GeoIndex(indexes.SearchIndex):
	model = None
	text = indexes.CharField(document=True, use_template=True)
	lat = indexes.DecimalField(model_attr='lat')
	lon = indexes.DecimalField(model_attr='lon')
	location = indexes.LocationField(model_attr='get_location')

class PersonIndex(GeoIndex, indexes.SearchIndex, indexes.Indexable):
	gender = indexes.CharField(model_attr='gender',null=True)
	organisation = indexes.CharField(model_attr='organization',null=True)
	department = indexes.CharField(model_attr='department',null=True)
	title = indexes.CharField(model_attr='title',null=True)
	# employeeID = indexes.CharField(model_attr='employeeID',null=True)
	# studentID = indexes.CharField(model_attr='studentID',null=True)
	lastModified = indexes.DateTimeField(model_attr='lastModified')

	def get_model(self):
		return Person

class BuildingIndex(GeoIndex, indexes.SearchIndex, indexes.Indexable):
	abbr = indexes.CharField(model_attr='abbreviation')
	name = indexes.CharField(model_attr='name')
	address = indexes.CharField(model_attr='address')
	postalCode = indexes.CharField(model_attr='postalCode')
	city = indexes.CharField(model_attr='city')

	def get_model(self):
		return Building