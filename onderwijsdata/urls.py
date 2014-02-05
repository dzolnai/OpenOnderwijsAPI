from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'onderwijsdata.views.home', name='home'),
	url(r'^docs/', include('rest_framework_swagger.urls')),
	url(r'^',      include('api.urls')),
	url(r'^oauth2/', include('provider.oauth2.urls', namespace='oauth2')),
	url(r'^admin/', include(admin.site.urls)),
	
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
