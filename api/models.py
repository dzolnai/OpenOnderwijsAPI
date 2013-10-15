from django.db import models


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
	title   = models.CharField(max_length=255)
	#updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('title',)

	def last_updated(self):
		my_items = NewsItem.objects.filter(feeds=self)
		if my_items.count()==0: return None
		return my_items.order_by('-pubDate')[0].pubDate


