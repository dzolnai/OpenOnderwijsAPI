from django.db import models
from django.utils import timezone
from django.db import models
from haystack.utils.geo import Point
from django.core.validators import MaxValueValidator


def selfzip(a):
    return zip(a, a)


class NewsItem(models.Model):
    newsitemId = models.AutoField(primary_key=True)
    publishDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    content = models.TextField()
    feeds = models.ManyToManyField('NewsFeed', related_name='items',blank=True, null=True)
    #lastModified = models.DateTimeField(auto_now=True, default=timezone.now())

    class Meta:
        ordering = ('pubDate',)


class NewsFeed(models.Model):
    newsfeedId  = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    items = models.ForeignKey('NewsItem')
    groups = models.ManyToManyField('NewsItem', related_name='newsfeeds',blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())

    # updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def last_updated(self):
        my_items = NewsItem.objects.filter(feeds=self)
        if my_items.count() == 0: return None
        return my_items.order_by('-pubDate')[0].pubDate


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

        # cluster
        # education
        # klas  # LesGroep
        # groups          = models.ManyToManyField('Group',through='GroupRole')
        # altitude        = models.DecimalField(max_digits=3,decimal_places=2,blank=True,null=True)
        # employeeID      = models.CharField(blank=True,null=True,max_length=255)  # only for affiliation=employee
        # studentID       = models.CharField(blank=True,null=True,max_length=255)  # only for affiliation=student


class Group(models.Model):
    GROUP_TYPES = ('?LesGroep', '?LeerGroep', 'ou', 'affiliation', 'Generic')

    groupId       = models.AutoField(primary_key=True)
    type          = models.CharField(max_length=32, choices=selfzip(GROUP_TYPES))
    name          = models.CharField(max_length=255)
    description   = models.TextField(blank=True, null=True)
    lastModified  = models.DateTimeField(auto_now=True, default=timezone.now())
    members       = models.ManyToManyField('Person', through='GroupRole', blank=True, null=True)
    courses       = models.ForeignKey('Course', related_name='groups')
    lastModified  = models.DateTimeField(auto_now=True,default=timezone.now())

class GroupRole(models.Model):
    ROLES = ('member', 'manager', 'administrator')

    grouproleId   = models.AutoField(primary_key=True)
    person        = models.ForeignKey('Person', related_name='groups')
    group         = models.ForeignKey('Group', related_name='members')
    roles         = models.CharField(choices=selfzip(ROLES), max_length=32)
    lastModified  = models.DateTimeField(auto_now=True,default=timezone.now())

    class Meta:
        unique_together = ('person', 'group')

    def groupName(self):
        return self.group.name

    def groupType(self):
        return self.group.type

    def displayName(self):
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

    # lastModified = models.DateTimeField(auto_now=True,default=timezone.now())

    def get_location(self):
        return Point(float(self.lon), float(self.lat))


class Room(models.Model):
    roomId = models.AutoField(primary_key=True)
    buildingId = models.ForeignKey('Building', related_name='rooms')
    abbreviation = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    totalSeats = models.PositiveIntegerField(blank=True, null=True)
    totalWorkspaces = models.PositiveIntegerField(blank=True, null=True)
    availableWorkspaces = models.PositiveIntegerField(blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    # type              = models.TextField()
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    altitude = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)


class Course(models.Model):
    LEVELS = ('HBO-B', 'HBO-M', 'WO-B', 'WO-M', 'WO-D')
    LANGUAGES = ('nl-NL', 'en-GB', 'de-DE')
    schedules = models.ForeignKey('Schedule', related_name='schedules')
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
    lecturers = models.ForeignKey('Person', related_name='courses')
    groups = models.ManyToManyField('Group', related_name='courses')
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())


# feeds   = models.ManyToManyField('Minor',related_name='courses')


class Lesson(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    course = models.ForeignKey('Course', related_name='lessons')
    room = models.ForeignKey('Room', related_name='lessons')
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
    # student       = models.ForeignKey('Person')
    courseId = models.ForeignKey('Course')
    courseResult = models.ForeignKey('CourseResult', blank=True, null=True, related_name='testResults')
    userId = models.ForeignKey('Person')
    description = models.CharField(max_length=255)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    testDate = models.DateField()
    # grade         = models.DecimalField(max_digits=3,decimal_places=2,blank=True,null=True)
    grade = models.CharField(max_length=255)
    comment = models.TextField()
    # result        = models.CharField(max_length=15,blank=True,null=True)
    passed = models.NullBooleanField()
    weight = models.PositiveIntegerField(min_value=0, validators=[MaxValueValidator(100), ], blank=True, null=True)


class CourseResult(models.Model):
    student = models.ForeignKey('Person')
    course = models.ForeignKey('Course')
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
    grade = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    result = models.CharField(blank=True, null=True, max_length=15)
    passed = models.NullBooleanField()


class Schedule(models.Model):
    scheduleId = models.AutoField(primary_key=True)
    userId = models.ForeignKey('Person', related_name='schedules', blank=True, null=True, )
    roomId = models.ForeignKey('Room', related_name='schedules', blank=True, null=True, )
    buildingId = models.ForeignKey('Building', related_name='schedules', blank=True, null=True)
    courseId = models.ForeignKey('Course', related_name='schedules', blank=True, null=True)
    startDateTime = models.DateTimeField(blank=True, null=True)
    endDateTime = models.DateTimeField(blank=True, null=True)
    groupId = models.ForeignKey('Group', related_name='groups', blank=True, null=True)
    lecturers = models.ForeignKey('Person', related_name='lecturer', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lastModified = models.DateTimeField(auto_now=True, default=timezone.now())
