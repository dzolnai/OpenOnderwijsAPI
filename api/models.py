from api.custom_fields import ListField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from haystack.utils.geo import Point


def selfzip(a):
    return zip(a, a)


class NewsItem(models.Model):
    newsitemId = models.AutoField(primary_key=True)
    publishDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    authors = ListField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    content = models.TextField()
    feeds = models.ManyToManyField('NewsFeed', through='NewsItemFeedRelation', related_name="+")

    class Meta:
        ordering = ('publishDate',)


class NewsFeed(models.Model):
    newsfeedId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField('Group', related_name='feeds', blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    items = models.ManyToManyRel('NewsItem', through='NewsItemFeedRelation', related_name="+")

    class Meta:
        ordering = ('lastModified',)

    def last_updated(self):
        my_items = NewsItem.objects.filter(feeds=self)
        if my_items.count() == 0: return None
        return my_items.order_by('-pubDate')[0].pubDate


class NewsItemFeedRelation(models.Model):
    newsItemFeedRelationId = models.AutoField(primary_key=True)
    newsFeedId = models.ForeignKey('NewsFeed')
    newsItemId = models.ForeignKey('NewsItem')

    class Meta:
        auto_created=True


class Affiliation(models.Model):
    AFFILIATIONS = ('student', 'faculty', 'staff', 'alum', 'member', 'affiliate', 'employee')
    affiliation = models.CharField(choices=selfzip(AFFILIATIONS), max_length=9, help_text='as defined in eduPerson')


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
    gender = models.CharField(blank=True, null=True, choices=selfzip(GENDERS), max_length=1)
    organization = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True, help_text='job title and/or description')
    office = models.ForeignKey('Room', blank=True, null=True)
    groups = models.ManyToManyField('Group', through='GroupRole')
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())

    def get_location(self):
        return Point(float(self.lon), float(self.lat))


class Group(models.Model):
    GROUP_TYPES = ('?LesGroep', '?LeerGroep', 'ou', 'affiliation', 'Generic')

    groupId = models.AutoField(primary_key=True)
    type = models.CharField(max_length=32, choices=selfzip(GROUP_TYPES))
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    members = models.ManyToManyField('Person', through='GroupRole', blank=True, null=True)


class GroupRole(models.Model):
    ROLES = ('member', 'manager', 'administrator')
    grouproleId = models.AutoField(primary_key=True)
    person = models.ForeignKey('Person', related_name='person')
    group = models.ForeignKey('Group', related_name='group')
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    roles = ListField(choices=selfzip(ROLES), null=False, blank=False)

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
    lat = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    lon = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)

    def get_location(self):
        return Point(float(self.lon), float(self.lat))


class Room(models.Model):
    roomId = models.AutoField(primary_key=True)
    buildingId = models.ForeignKey('Building', related_name='room_building_id')
    abbreviation = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    totalSeats = models.PositiveIntegerField(blank=True, null=True)
    totalWorkspaces = models.PositiveIntegerField(blank=True, null=True)
    availableWorkspaces = models.PositiveIntegerField(blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    altitude = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)


class Course(models.Model):
    LEVELS = ('HBO-B', 'HBO-M', 'WO-B', 'WO-M', 'WO-D')
    LANGUAGES = ('nl-NL', 'en-GB', 'de-DE')
    schedules = models.ManyToManyField('Schedule', through='CourseScheduling', related_name='+', blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=32, unique=True, blank=True, null=True)
    ects = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField()
    goals = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    level = models.CharField(choices=selfzip(LEVELS), max_length=8)
    format = models.TextField(blank=True, null=True)
    language = models.CharField(choices=selfzip(LANGUAGES), max_length=2)
    enrollment = models.TextField(blank=True, null=True)
    literature = models.TextField(blank=True, null=True)
    exams = models.TextField(blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    lecturers = models.ForeignKey('Person', related_name='courses', blank=True, null=True)
    groups = models.ManyToManyField('Group', related_name='courses', blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())


# feeds   = models.ManyToManyField('Minor',related_name='courses')


class Lesson(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    course = models.ForeignKey('Course', related_name='course')
    room = models.ForeignKey('Room', related_name='room')
    description = models.TextField(blank=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())


# ??
class Minor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    courses = models.ManyToManyField('Course', related_name='minors')
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())


class TestResult(models.Model):
    testResultId = models.AutoField(primary_key=True)
    courseId = models.ForeignKey('Course')
    courseResult = models.ForeignKey('CourseResult', blank=True, null=True, related_name='courseResult')
    userId = models.ForeignKey('Person')
    description = models.CharField(max_length=255)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    testDate = models.DateField()
    grade = models.CharField(max_length=255)
    comment = models.TextField()
    passed = models.NullBooleanField()
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(100), ], blank=True, null=True)


class CourseResult(models.Model):
    student = models.ForeignKey('Person')
    course = models.ForeignKey('Course')
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    grade = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    result = models.CharField(blank=True, null=True, max_length=15)
    passed = models.NullBooleanField()


class Schedule(models.Model):
    scheduleId = models.AutoField(primary_key=True)
    userId = models.ForeignKey('Person', related_name='schedule_user', blank=True, null=True, )
    roomId = models.ForeignKey('Room', related_name='schedule_room', blank=True, null=True, )
    buildingId = models.ForeignKey('Building', related_name='schedule_building_id', blank=True, null=True)
    courseId = models.ManyToManyField('Course', through='CourseScheduling', related_name='+', blank=True, null=True)
    startDateTime = models.DateTimeField(blank=True, null=True)
    endDateTime = models.DateTimeField(blank=True, null=True)
    groupId = models.ForeignKey('Group', related_name='schedule_group_id', blank=True, null=True)
    lecturers = models.ForeignKey('Person', related_name='schedule_lecturer_id', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())


class CourseScheduling(models.Model):
    courseSchedulingId = models.AutoField(primary_key=True)
    course = models.ForeignKey('Course')
    schedule = models.ForeignKey('Schedule')

    class Meta:
        auto_created = True
