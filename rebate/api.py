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
		always_return_data = True
		include_resource_uri = False

class UtilitiesResource(ModelResource):
	### this works, just turned off because it returns to many records
	# ziputilities = fields.ToManyField('rebate.api.ZipUtilitiesResource', 'ziputilities_set', related_name='ziputils')
	###
	# # rebateprograms = fields.ToManyField('rebate.api.RebateProgramsResource', 'rebateprograms_set', full=True)
	class Meta: 
		queryset = Utilities.objects.all()
		resource_name = 'utilities'
		excludes = excluded_fields()

class UtilityProgramsResource(ModelResource):
	rebateprograms = fields.ToManyField('rebate.api.RebateProgramsResource', 'rebateprograms_set', full=True)
	
	class Meta: 
		queryset = Utilities.objects.all()
		resource_name = 'utilityprograms'
		excludes = excluded_fields()	
  
class ZipUtilitiesResource(ModelResource):
	utility = fields.ToOneField('rebate.api.UtilitiesResource', 'utility', related_name='zipcodes', full=True)
	energytype = fields.ForeignKey('rebate.api.EnergyTypesResource', 'energytype', related_name='zipcodes', full=True)
	# # utilitytype = fields.ForeignKey('rebate.api.UtilityTypesResource', 'utilitytype', related_name='zipcodes', full=True)

	
	class Meta:
		queryset = ZipUtilities.objects.all().filter(Q(overlap=1) | Q(overlap=0)).order_by('-overlap')
		resource_name = 'ziputilities'
		excludes = excluded_fields()#.append('overlap')
		filtering = {
			"zipcode": ('exact'),
			"energytype": ('exact'),
		}
		serializer = PrettyJSONSerializer()



class ElecUtilitiesResource(ModelResource):
	utility = fields.ToOneField('rebate.api.UtilitiesResource', 'utility', related_name='zipcodes', full=True)
	# # energytype = fields.ForeignKey('rebate.api.EnergyTypesResource', 'energytype', related_name='zipcodes', full=True)
	# # utilitytype = fields.ForeignKey('rebate.api.UtilityTypesResource', 'utilitytype', related_name='zipcodes', full=True)

	
	class Meta:
		queryset = ZipUtilities.objects.all().filter(Q(overlap=1) | Q(overlap=0), Q(energytype_id=2)).order_by('-overlap')
		resource_name = 'elec_utilities'
		excludes = excluded_fields()#.append('overlap')
		filtering = {
			"zipcode": ('exact'),
			# # "energytype": ('exact'),
		}
		serializer = PrettyJSONSerializer()

		
class GasUtilitiesResource(ModelResource):
	utility = fields.ToOneField('rebate.api.UtilitiesResource', 'utility', related_name='zipcodes', full=True)
	energytype = fields.ForeignKey('rebate.api.EnergyTypesResource', 'energytype', related_name='zipcodes', full=True)
	# # utilitytype = fields.ForeignKey('rebate.api.UtilityTypesResource', 'utilitytype', related_name='zipcodes', full=True)

	
	class Meta:
		queryset = ZipUtilities.objects.all().filter(Q(overlap=1) | Q(overlap=0), Q(energytype_id=3)).order_by('-overlap')
		resource_name = 'gas_utilities'
		excludes = excluded_fields()
		excludes.append('energytype')
		filtering = {
			"zipcode": ('exact'),
		}
		serializer = PrettyJSONSerializer()

		
class EnergyTypesResource(ModelResource):
	
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
	
	
	class Meta:
		queryset = RebatePrograms.objects.all()
		resource_name = 'rebateprograms' 		# for URL
		excludes = excluded_fields()

	def dehydrate(self, bundle):
		print bundle.request.path
		if self.get_resource_uri(bundle) != bundle.request.path:
			del bundle.data['rebateprogramtechnologies'] 
		return bundle
		