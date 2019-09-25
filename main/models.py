from django.db import models
from datetime import datetime
# Create your models here.

class TutorialCategory(models.Model):
	category 	= models.CharField(max_length=200)
	summery 	= models.CharField(max_length=200)
	slug 		= models.CharField(max_length=200)
	
	class Meta:
		verbose_name_plural = "categories"

	def __str__(self):
		return self.category


class TutorialSeries(models.Model):
	tutorial_series  	= models.CharField(max_length=200)
	tutorial_category	= models.ForeignKey(TutorialCategory, default=1, verbose_name="category", on_delete=models.SET_DEFAULT)
	series_summery  	= models.CharField(max_length=200)
	
	class Meta:
		verbose_name_plural = "series"

	def __str__(self):
		return self.tutorial_series



class Tutorial(models.Model):
	tutorial_title 		= models.CharField(max_length=200)
	tutorial_content 	= models.TextField()
	tutorial_published 	= models.DateTimeField("date puplished:")
	tutorial_series		= models.ForeignKey(TutorialSeries, default=1, verbose_name="series", on_delete=models.SET_DEFAULT)
	tutorial_slug 		= models.CharField(max_length=200, unique=True)



	def __str__(self):
		return self.tutorial_title

	# def save(self, **kwargs):
	# 	tutorial_slug = '%s' % (self.tutorial_title)
	# 	unique_slugify(self, tutorial_slug)
	# 	super(Tutorial, self).save()