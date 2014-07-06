from django.db import models

# Create your models here.
class Zipcodes(models.Model):
	zipcode = models.CharField(max_length=5)
	state = models.CharField(max_length=2)
	city = models.CharField(max_length=100)
	type = models.CharField(max_length=1)
	countyfips = models.CharField(max_length=5)
	latitude = models.FloatField()
	longitude = models.FloatField()
	areacode = models.CharField(max_length=3)
	financecode = models.CharField(max_length=6)
	lastline = models.CharField(max_length=4, null=True)
	fac = models.CharField(max_length=1, null=True)
	msa = models.CharField(max_length=4, null=True)
	pmsa = models.CharField(max_length=4, null=True)
	modifieduser = models.CharField(max_length=128, default='admin')
	modifieddate = models.DateField(auto_now=True)

	def __unicode__(self):
		return self.zipcode

class Utilities(models.Model):
	utilityname = models.CharField(max_length=50)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
	# recordstatus = models.ForeignKey(RecordStatus)
	
	def __unicode__(self):
		return self.utilityname
		
class ProgramAdmins(models.Model):
	name = models.CharField(max_length=500, null=True)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)

class FundingSources(models.Model):
	name = models.CharField(max_length=100, null=True)
	notes = models.CharField(max_length=1000, null=True)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)

class ProgramStatuses(models.Model):
	description = models.CharField(max_length=255)
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	comments = models.CharField(max_length=100, null=True)
	img = models.CharField(max_length=100, null=True)

class States(models.Model):
	abbr = models.CharField(max_length=2)
	name = models.CharField(max_length=35)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)

class RecordStatus(models.Model):
	description = models.CharField(max_length=50)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
	statuscode = models.CharField(max_length=20)

class TechnologyCategories(models.Model):
	name = models.CharField(max_length=50)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
'''
sectors #
technology categories #
technologies #
fundingtypes #

rebateprograms_sector #
rebateprograms_technologies #
rebateprograms_fundingtypes

####
next steps
####
drop table RebateProgram_Technologies
reload the class RebatePrograms_Technologies to keep the syntax
next, import these csv's. 


'''
class Sectors(models.Model):
	name = models.CharField(max_length=50, null=True)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)

class Technologies(models.Model):
	name = models.CharField(max_length=100, null=True)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)	
	techologycategory = models.ForeignKey(TechnologyCategories)
	
class FundingTypes(models.Model):
	description = models.CharField(max_length=100, null=True)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
	
class RebatePrograms(models.Model):
	name = models.CharField(max_length=500)
	state = models.ForeignKey(States)
	fundingsource = models.ForeignKey(FundingSources)
	programyearstartdate = models.DateField(null=True)
	programyearenddate = models.DateField(null=True)
	programstartdatestring = models.TextField(max_length=1000, null=True)
	programenddatestring = models.TextField(max_length=1000, null=True)
	recordstatus = models.ForeignKey(RecordStatus)
	programstatus = models.ForeignKey(ProgramStatuses)
	programadmin = models.ForeignKey(ProgramAdmins)
	website = models.URLField(max_length=1000, null=True)
	temppayoutstring = models.TextField(null=True)
	tempprojectsizestring = models.TextField(max_length=1000, null=True)
	temprequirementsstring = models.TextField(max_length=1500, null=True)
	programcaveats = models.TextField(max_length=1000, null=True)
	programbudget = models.CharField(max_length=255, null=True)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
	utilities = models.ManyToManyField(Utilities)
	sectors = models.ManyToManyField(Sectors)
	fundingtypes = models.ManyToManyField(FundingTypes)

class RebatePrograms_Technologies(models.Model):
	rebateprogram = models.ForeignKey('RebatePrograms', related_name='rebateprogramtechnologies')
	technologies = models.ForeignKey('Technologies', related_name='rebateprogramtechnologies')
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
	directory_url = models.URLField(max_length=1000, null=True)
	application_url = models.URLField(max_length=1000, null=True)
	caps = models.TextField(max_length=1000, null=True)
	payout_overview = models.TextField(max_length=1000, null=True)	
	
class EnergyTypes(models.Model):
	energy = models.CharField(max_length=50)
	# description = models.CharField(max_length=128)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)
	code = models.CharField(max_length=5)
	
class UtilityTypes(models.Model):
	code = models.CharField(max_length=10)
	description = models.CharField(max_length=50)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)

class ZipUtilities(models.Model):
	zipcode = models.CharField(max_length=5)
	overlap = models.FloatField(default=1)
	energytype = models.ForeignKey(EnergyTypes)
	utilitytype = models.ForeignKey(UtilityTypes)
	recordstatus = models.ForeignKey(RecordStatus)
	utility = models.ForeignKey(Utilities)
	createduser = models.CharField(max_length=50)
	createddate = models.DateField(auto_now_add=True)
	modifieduser = models.CharField(max_length=50, default='admin')
	modifieddate = models.DateField(auto_now=True)

	
'''
sectors
technology categories
technologies
fundingtypes

rebateprogramsectors
rebateprogramtechnologies
rebateprogramfundingtypes
'''
	
'''
SELECT --[MapInfoId]
      [ZipCode]
      --,[UtilityId]
      ,[Overlap]
      ,[EnergyTypeId]
      ,[UtilityTypeId]
      ,[RecordStatusId]
      ,[RWWUtilityId] UtilityId
      ,[CreatedUser]
      ,[CreatedDate]
      ,[ModifiedUser]
      ,[ModifiedDate]
      --,[EmployeeId]
  FROM [RebatePrograms].[dbo].[ZipUtilities]
'''
	
	

	