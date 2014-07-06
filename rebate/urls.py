from django.conf.urls import patterns, include, url
from tastypie.api import Api
from rebate.api import ZipcodesResource, ZipUtilitiesResource, UtilitiesResource, EnergyTypesResource, UtilityTypesResource, RebateProgramsResource, SectorsResource, TechnologiesResource, RebateProgramTechnologiesResource, ElecUtilitiesResource, GasUtilitiesResource, UtilityProgramsResource


v1_api = Api(api_name='api')
v1_api.register(ZipcodesResource())
v1_api.register(ZipUtilitiesResource())
v1_api.register(UtilitiesResource())
v1_api.register(EnergyTypesResource())
v1_api.register(UtilityTypesResource())
v1_api.register(RebateProgramsResource())
v1_api.register(SectorsResource())
v1_api.register(TechnologiesResource())
v1_api.register(RebateProgramTechnologiesResource())
v1_api.register(ElecUtilitiesResource())
v1_api.register(GasUtilitiesResource())
v1_api.register(UtilityProgramsResource())

urlpatterns = patterns('',
	url(r'', include(v1_api.urls)),
	url(r'^zip/(?P<zipcode>)/', include(v1_api.urls)),
	# these urls are automagically created by our ModelResource class from api.py
)