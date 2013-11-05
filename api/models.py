from django.db import models

def selfzip(a):
	return zip(a,a)

class NewsItem(models.Model):
	pubDate = models.DateTimeField(auto_now_add=True)
	title   = models.CharField(max_length=255)
	author  = models.CharField(max_length=255)
	image   = models.URLField()
	link    = models.URLField()
	content = models.TextField()
	feeds   = models.ManyToManyField('NewsFeed',related_name='items')

	class Meta:
		ordering = ('pubDate',)


class NewsFeed(models.Model):
	title       = models.CharField(max_length=255)
	description = models.TextField(blank=True)
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
	mail            = models.EmailField(blank=False)
	telephoneNumber = models.CharField(blank=True,max_length=32)  #models.TelephoneField() IETU E.123 
	mobileNumber    = models.CharField(blank=True,max_length=32)  #models.TelephoneField()
	photo           = models.URLField(blank=True)
	gender          = models.CharField(blank=True,choices=selfzip(GENDERS),max_length=1)
	organisation    = models.TextField(blank=True,)
	department      = models.TextField(blank=True,help_text='ou in X.520')  #multivalued
	title           = models.TextField(blank=True,help_text='job title and/or description')
	office          = models.TextField(blank=True)
	employeeID      = models.CharField(blank=True,max_length=255)  # only for affiliation=employee
	studentID       = models.CharField(blank=True,max_length=255)  # only for affiliation=student
	#cluster
	#education
	#klas  # LesGroep
	#groups          = models.ManyToManyField('Group',through='GroupRole')


class Group(models.Model):
	GROUP_TYPES = ('?LesGroep','?LeerGroep','ou','affiliation','Generic')

	type        = models.CharField(max_length=32,choices=selfzip(GROUP_TYPES))
	name        = models.CharField(blank=True,max_length=255)
	description = models.TextField(blank=True)
	#members     = models.ManyToManyField('Person',through='GroupRole')

class GroupRole(models.Model):
	ROLES = ('member','manager','administrator')

	person = models.ForeignKey(Person,related_name='groups')
	group  = models.ForeignKey(Group,related_name='members')
	role   = models.CharField(choices=selfzip(ROLES),max_length=32)

	class Meta:
		unique_together = ('person','group')

	def groupName(self):
		return self.group.name
	def groupType(self):
		return self.group.type
	def displayName(self):
		return self.person.displayName


