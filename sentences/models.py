from django.db import models
import datetime

# Create your models here.

# Sentence
class Sentence(models.Model):
	sentence = models.CharField(max_length=200) #the sentence
	
	#other info
	pub_date = models.DateTimeField("Date Submitted")
	
	#Display something useful at interactive prompt...
	def __unicode__(self):
		return self.sentence
		
	#Helper functions --------------------------------------------------
	#TimeSinceSubmitted - returns a string describing how long since the
	#                     sentence was submitted
	def TimeSinceSubmitted(self):
		return datetime.datetime.now() - self.pub_date.date()
	TimeSinceSubmitted.short_description = "Time Since submitted"

# Media
class Media(models.Model):
	file = models.FileField(upload_to="Sentences/Files", blank=True) #the location of the file
	image = models.ImageField(upload_to="Sentences/Images", blank=True) #the location of the image (if it is an image)
	
	TYPE_CHOICES = (
		('Sound', 'Sound'),
		('Image', 'Image'),
		('Video', 'Video'),
	)
	
	#type of Media
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
			
	#Relationships
	sentence = models.ForeignKey(Sentence)
