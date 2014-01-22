from django.db import models

def selfzip(a):
	return zip(a,a)

class NewsItem(models.Model):
	pubDate = models.DateTimeField(auto_now_add=True)
	title   = models.CharField(max_length=255)
	author  = models.CharField(max_length=255,blank=True,null=True)
	image   = models.URLField(blank=True,null=True)
	link    = models.URLField()
	content = models.TextField()
	feeds   = models.ManyToManyField('NewsFeed',related_name='items')

	class Meta:
		ordering = ('pubDate',)


class NewsFeed(models.Model):
	title       = models.CharField(max_length=255)
	description = models.TextField(blank=True,null=True)
	#updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('title',)

	def last_updated(self):
		my_items = NewsItem.objects.filter(feeds=self)
		if my_items.count()==0: return None
		return my_items.order_by('-pubDate')[0].pubDate


class Affiliation(models.Model):
	AFFILIATIONS=('student','faculty','staff','alum','member','affiliate','employee')
	affiliation = models.CharField(choices=selfzip(AFFILIATIONS),max_length=9,help_text='as defined in eduPerson')

class Person(models.Model):
	GENDERS=('M','F')

	""" Required attributes """
	givenName       = models.CharField(max_length=255)
	surName         = models.CharField(max_length=255,help_text='in X.520 this attribute is called sn')
	displayName     = models.CharField(max_length=255)
	affiliations    = models.ManyToManyField('Affiliation',related_name='persons')

	""" Optional attributes """
	mail            = models.EmailField(blank=True,null=True)
	telephoneNumber = models.CharField(blank=True,null=True,max_length=32)  #models.TelephoneField() IETU E.123 
	mobileNumber    = models.CharField(blank=True,null=True,max_length=32)  #models.TelephoneField()
	photo           = models.URLField(blank=True,null=True)
	gender          = models.CharField(blank=True,null=True,choices=selfzip(GENDERS),max_length=1)
	organisation    = models.CharField(max_length=255,blank=True,null=True,)
	department      = models.CharField(max_length=255,blank=True,null=True,help_text='ou in X.520')  #multivalued
	title           = models.CharField(max_length=255,blank=True,null=True,help_text='job title and/or description')
	office          = models.ForeignKey('Room',blank=True,null=True)
	employeeID      = models.CharField(blank=True,null=True,max_length=255)  # only for affiliation=employee
	studentID       = models.CharField(blank=True,null=True,max_length=255)  # only for affiliation=student
	#cluster
	#education
	#klas  # LesGroep
	#groups          = models.ManyToManyField('Group',through='GroupRole')


class Group(models.Model):
	GROUP_TYPES = ('?LesGroep','?LeerGroep','ou','affiliation','Generic')

	type        = models.CharField(max_length=32,choices=selfzip(GROUP_TYPES))
	name        = models.CharField(max_length=255)
	description = models.TextField(blank=True,null=True)
	#members     = models.ManyToManyField('Person',through='GroupRole')

class GroupRole(models.Model):
	ROLES = ('member','manager','administrator')

	person = models.ForeignKey('Person',related_name='groups')
	group  = models.ForeignKey('Group',related_name='members')
	role   = models.CharField(choices=selfzip(ROLES),max_length=32)

	class Meta:
		unique_together = ('person','group')

	def groupName(self):
		return self.group.name
	def groupType(self):
		return self.group.type
	def displayName(self):
		return self.person.displayName

class Building(models.Model):
	abbr        = models.CharField(primary_key=True,max_length=32)
	name        = models.CharField(max_length=256)
	description = models.TextField()
	address     = models.CharField(max_length=256)
	postalCode  = models.CharField(max_length=16)
	city		= models.CharField(max_length=255)
	lat         = models.DecimalField(max_digits=9,decimal_places=6)
	lon         = models.DecimalField(max_digits=9,decimal_places=6)

class Room(models.Model):
	building            = models.ForeignKey('Building',related_name='rooms')
	abbr                = models.CharField(primary_key=True,max_length=32)
	name                = models.CharField(max_length=255,blank=True)
	description         = models.TextField(blank=True,null=True)
	totalSeats          = models.PositiveIntegerField(blank=True,null=True)
	totalWorkspaces     = models.PositiveIntegerField(blank=True,null=True)
	availableWorkspaces = models.PositiveIntegerField(blank=True,null=True)
	# type              = models.TextField()

class Course(models.Model):
	LEVELS    = ('HBO-B','HBO-M','WO-B','WO-M','WO-D')
	LANGUAGES = ('nl','en','de')
	name         = models.CharField(max_length=255,unique=True)
	abbr         = models.CharField(max_length=32,unique=True)
	ects         = models.PositiveIntegerField()
	description  = models.TextField()
	goals        = models.TextField(blank=True,null=True)
	requirements = models.TextField(blank=True,null=True)
	level        = models.CharField(choices=selfzip(LEVELS),max_length=8)
	format       = models.TextField(blank=True,null=True)
	language     = models.CharField(choices=selfzip(LANGUAGES),max_length=2)
	enrollment   = models.TextField(blank=True,null=True)
	literature   = models.TextField(blank=True,null=True)
	exams        = models.TextField(blank=True,null=True)
	schedule     = models.TextField(blank=True,null=True)
	url          = models.URLField(blank=True,null=True)
	organisation = models.CharField(max_length=255,blank=True,null=True)
	department   = models.CharField(max_length=255,blank=True,null=True)
	lecturers    = models.ForeignKey('Person',related_name='courses')



#	feeds   = models.ManyToManyField('Minor',related_name='courses')

#??
class Minor(models.Model):
	name = models.CharField(max_length=244,unique=True)
