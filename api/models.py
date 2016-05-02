from api.custom_fields import ListField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from haystack.utils.geo import Point


def self_zip(a):
    return zip(a, a)


class NewsItem(models.Model):
    newsitemId = models.AutoField(primary_key=True)
    publishDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    authors = ListField(blank=True, null=True, max_length=255)
    image = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    content = models.TextField()
    feeds = models.ManyToManyField('NewsFeed', related_name="items")

    class Meta:
        ordering = ('publishDate',)


class NewsFeed(models.Model):
    newsfeedId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField('Group', related_name='feeds')
    lastModified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('lastModified',)


class Affiliation(models.Model):
    AFFILIATIONS = ('student', 'faculty', 'staff', 'alum', 'member', 'affiliate', 'employee')
    affiliation = models.CharField(choices=self_zip(AFFILIATIONS), max_length=9, help_text='as defined in eduPerson',
                                   primary_key=True)


class Person(models.Model):
    GENDERS = ('M', 'F', 'U', 'X')

    """ Required attributes """
    userId = models.AutoField(primary_key=True)
    givenname = models.CharField(max_length=255)
    surname = models.CharField(max_length=255, help_text='in X.520 this attribute is called sn')
    displayname = models.CharField(max_length=255)
    affiliations = models.ManyToManyField('Affiliation', related_name='persons')

    """ Optional attributes """
    commonname = models.CharField(blank=True, null=True, max_length=255)
    nickname = models.CharField(blank=True, null=True, max_length=255)
    mail = models.EmailField(blank=True, null=True)
    telephonenumber = models.CharField(blank=True, null=True, max_length=32)  # models.TelephoneField() IETU E.123
    mobilenumber = models.CharField(blank=True, null=True, max_length=32)  # models.TelephoneField()
    photoSocial = models.URLField(blank=True, null=True)
    photoOfficial = models.URLField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, choices=self_zip(GENDERS), max_length=1)
    organization = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True, help_text='job title and/or description')
    office = models.ForeignKey('Room', blank=True, null=True)
    lat = models.DecimalField(max_digits=8, decimal_places=5)
    lon = models.DecimalField(max_digits=8, decimal_places=5)
    lastModified = models.DateTimeField(auto_now=True)

    def get_location(self):
        return Point(float(self.lon), float(self.lat))


class Group(models.Model):
    GROUP_TYPES = ('?LesGroep', '?LeerGroep', 'ou', 'affiliation', 'Generic')

    groupId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=32, choices=self_zip(GROUP_TYPES))
    courses = models.ManyToManyField('Course', related_name="groups")
    members = models.ManyToManyField('Person', through='GroupRole', related_name="groups")
    lastModified = models.DateTimeField(auto_now=True)


class GroupRole(models.Model):
    ROLES = ('member', 'manager', 'administrator')
    grouproleId = models.AutoField(primary_key=True)
    person = models.ForeignKey('Person', related_name='person')
    group = models.ForeignKey('Group', related_name='group')
    lastModified = models.DateTimeField(auto_now=True)
    roles = ListField(choices=self_zip(ROLES), null=False, blank=False, max_length=255)

    class Meta:
        unique_together = ('person', 'group')

    def group_name(self):
        return self.group.name

    def group_type(self):
        return self.group.type

    def display_name(self):
        return self.person.displayname


class Building(models.Model):
    buildingId = models.AutoField(primary_key=True)
    abbreviation = models.CharField(max_length=32)
    name = models.CharField(max_length=256)
    description = models.TextField()
    address = models.CharField(blank=True, null=True, max_length=256)
    postalCode = models.CharField(blank=True, null=True, max_length=16)
    city = models.CharField(max_length=255)
    lat = models.DecimalField(max_digits=8, decimal_places=5)
    lon = models.DecimalField(max_digits=8, decimal_places=5)
    altitude = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True)

    def get_location(self):
        return Point(float(self.lon), float(self.lat))

    def complete_address(self):
        postal_code = self.postalCode if self.postalCode else ""
        city = self.city if self.city else ""
        address = self.address if self.address else ""
        if self.address is None:
            return postal_code + " " + city
        return address + ", " + postal_code + " " + city


class Room(models.Model):
    roomId = models.AutoField(primary_key=True)
    buildingId = models.ForeignKey('Building', related_name='room_building_id')
    abbreviation = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    totalSeats = models.PositiveIntegerField(blank=True, null=True)
    totalWorkspaces = models.PositiveIntegerField(blank=True, null=True)
    availableWorkspaces = models.PositiveIntegerField(blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    altitude = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True)


class Course(models.Model):
    LEVELS = ('HBO-B', 'HBO-M', 'WO-B', 'WO-M', 'WO-D')
    LANGUAGES = ('nl-NL', 'en-GB', 'de-DE')
    courseId = models.TextField(blank=False, null=False, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=32, unique=True, blank=True, null=True)
    ects = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    goals = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    level = models.CharField(choices=self_zip(LEVELS), max_length=8)
    format = models.TextField(blank=True, null=True)
    language = models.CharField(choices=self_zip(LANGUAGES), max_length=2)
    enrollment = models.TextField(blank=True, null=True)
    literature = models.TextField(blank=True, null=True)
    exams = models.TextField(blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    lecturers = models.ForeignKey('Person', related_name='courses', blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-lastModified']


# Not included in v1 API spec - do not remove, might be used in the future
class Minor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    courses = models.ManyToManyField('Course', related_name='minors')
    lastModified = models.DateTimeField(auto_now=True)


class TestResult(models.Model):
    testResultId = models.AutoField(primary_key=True)
    courseId = models.ManyToManyField('Course', related_name="testResults")
    userId = models.ManyToManyField('Person', related_name="testResults")
    description = models.CharField(max_length=255)
    lastModified = models.DateTimeField(auto_now=True)
    testDate = models.DateField()
    assessmentType = models.CharField(max_length=255)
    grade = models.CharField(max_length=255)
    comment = models.TextField()
    passed = models.NullBooleanField()
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(100), ], blank=True, null=True)


class Schedule(models.Model):
    scheduleId = models.AutoField(primary_key=True)
    userId = models.ManyToManyField('Person', related_name="+")
    roomId = models.ManyToManyField('Room', related_name='rooms')
    courseId = models.ManyToManyField('Course', related_name='schedules')
    startDateTime = models.DateTimeField(blank=True, null=True)
    endDateTime = models.DateTimeField(blank=True, null=True)
    groupId = models.ManyToManyField('Group', related_name="+")
    lecturers = models.ManyToManyField('Person', related_name="+")
    description = models.TextField(blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True)


class CourseResult(models.Model):
    courseResultId = models.AutoField(primary_key=True)
    student = models.ForeignKey('Person')
    course = models.ForeignKey('Course', blank=False, null=False)
    lastModified = models.DateTimeField(auto_now=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    comment = models.CharField(blank=True, null=True, max_length=15)
    passed = models.NullBooleanField()

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-lastModified"]
