from django.conf.urls import patterns, include, url
from django.contrib import admin
# from rebate.urls import v1_api
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rebates.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	
	url(r'^$', 'rebates.views.start', name='home'),
	url(r'^about/', 'rebates.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^api/', include('rebate.urls')),
	url(r'', include('rebate.urls')),
)
