from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.constants import ALL
from tastypie import fields
# constant ALL sets the types of query types we can perform on our models.
from models import Zipcodes, ZipUtilities, Utilities, EnergyTypes, UtilityTypes, RebatePrograms, Sectors, Technologies, RebatePrograms_Technologies

import json
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer

from django.db.models import Q

def excluded_fields():
	return ['createddate', 'createduser', 'modifieduser', 'id']
	
def excluded_fields2():
	excl = excluded_fields()
	excl.append('modifieddate')
	return excl

class PrettyJSONSerializer(Serializer):
    json_indent = 2

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(data, cls=DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

class ZipcodesResource(ModelResource):
	# util = fields.ToManyField('rebate.api.ZipUtilitiesResource', 'util', full=True)
	
	class Meta: 
		queryset = Zipcodes.objects.all().filter(Q(lastline='L')) #this is everything in the zipcodes table
		resource_name = 'zipcodes'
		# basically, this give the url path
		# localhost:8000/<project-level-url>/<app-level-url>/resource_name/
		filtering = {
			"zipcode": ('exact'),
		}
		serializer = PrettyJSONSerializer()
		excludes = excluded_fields()
	'''
	def dehydrate(self, bundle):
		print self["zipcode"]
		bundle.data['google_maps'] = 'whatever i want'
		return bundle
	'''	
class UtilitiesResource(ModelResource):
	### this works, just turned off because it returns to many records
	# ziputilities = fields.ToManyField('rebate.api.ZipUtilitiesResource', 'ziputilities_set', related_name='ziputils')
	###
	rebateprograms = fields.ToManyField('rebate.api.RebateProgramsResource', 'rebateprograms_set', full=True)
	class Meta: 
		queryset = Utilities.objects.all()
		resource_name = 'utilities'
		excludes = excluded_fields()
  
	# def override_urls(self):
		# return [url(r"^(?P<resource_name>%s)/(?P<utilityname>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),]
	
		
class ZipUtilitiesResource(ModelResource):
	utility = fields.ToOneField('rebate.api.UtilitiesResource', 'utility', related_name='zipcodes', full=True)
	energytype = fields.ForeignKey('rebate.api.EnergyTypesResource', 'energytype', related_name='zipcodes', full=True)
	utilitytype = fields.ForeignKey('rebate.api.UtilityTypesResource', 'utilitytype', related_name='zipcodes', full=True)
	# test = fields.CharField(null=True, default='blah')
	
	class Meta:
		queryset = ZipUtilities.objects.all().filter(Q(overlap=1) | Q(overlap=0)).order_by('-overlap')
		resource_name = 'ziputilities'
		excludes = excluded_fields()#.append('overlap')
		filtering = {
			"zipcode": ('exact'),
			"energytype": ('exact'),
		}
		serializer = PrettyJSONSerializer()
		#include_absolute_url = True
		# fields = ['zipcode', 'utility', 'utilitytype', 'energytype']

class EnergyTypesResource(ModelResource):
	# ziputilities = fields.ToManyField('rebate.api.ZipUtilitiesResource', 'ziputilities_set', related_name='energy_type', full=True, null=True)
	
	class Meta:
		queryset = EnergyTypes.objects.all()
		resource_name = 'energytypes'
		excludes = excluded_fields()

class UtilityTypesResource(ModelResource):
	
	class Meta:
		queryset = UtilityTypes.objects.all()
		resource_name = 'utilitytypes'
		excludes = excluded_fields()

class SectorsResource(ModelResource):
	
	class Meta:
		queryset = Sectors.objects.all()
		resource_name = 'sectors'
		excludes = excluded_fields2()
		include_resource_uri = False

class TechnologiesResource(ModelResource):
	
	class Meta:
		queryset = Technologies.objects.all()
		resource_name = 'technologies'
		excludes = excluded_fields2()
		include_resource_uri = False
		
class RebateProgramTechnologiesResource(ModelResource):
	# technologies = fields.ForeignKey('rebate.api.TechnologiesResource', 'technologies', related_name='rebateprograms', full=True)
	# rebateprogram = fields.ForeignKey('rebate.api.RebateProgramsResource', 'rebateprograms', related_name='rebateprograms', full=True)
	
	technology = fields.ForeignKey('rebate.api.TechnologiesResource', 'technologies', full=True)
	# rebateprogram = fields.ForeignKey('rebate.api.RebateProgramsResource', 'rebateprograms', full=True)
	
	class Meta:
		queryset = RebatePrograms_Technologies.objects.all()
		resource_name = 'rebateprogramtechnologies'
		excludes = excluded_fields()
		
		
class RebateProgramsResource(ModelResource):
	rebateprogramtechnologies = fields.ToManyField('rebate.api.RebateProgramTechnologiesResource', 'rebateprogramtechnologies', full=True)
	# utilities = fields.ToManyField('rebate.api.UtilitiesResource', 'utilities')
	# tech = fields.ToManyField('rebate.api.TechnologiesResource', 'technologies') 
	
	class Meta:
		queryset = RebatePrograms.objects.all()
		resource_name = 'rebateprograms'
		excludes = excluded_fields()


		
	# def prepend_urls(self):
		# return [
            # url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            # url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            # url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_multiple'), name="api_get_multiple"),
            # url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
		# ]

    # def determine_format(self, request):
        # """
        # Used to determine the desired format from the request.format
        # attribute.
        # """
        # if (hasattr(request, 'format') and
                # request.format in self._meta.serializer.formats):
            # return self._meta.serializer.get_mime_for_format(request.format)
        # return super(UserResource, self).determine_format(request)

    # def wrap_view(self, view):
        # @csrf_exempt
        # def wrapper(request, *args, **kwargs):
            # request.format = kwargs.pop('format', None)
            # wrapped_view = super(UserResource, self).wrap_view(view)
            # return wrapped_view(request, *args, **kwargs)
        # return wrapper
	# def dispatch(self, request_type, request, **kwargs):
		# zipcode = kwargs.pop('zipcode')
		# kwargs['zipcode'] = get_object_or_404(Zipcodes, zipcode = zipcode)
		# return super(ZipUtilities, self).dispatch(request_type, request, **kwargs)
		