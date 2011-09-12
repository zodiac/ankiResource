from django.db import models
from django.contrib.auth.models import User
import ankiResource
from ankiResource.sentences.models import Sentence

class Card(models.Model):
	# Relationships
	user = models.ForeignKey(User)
	sentence = models.ForeignKey(Sentence) #Media attached to this sentence
	
	# Values
	due = models.DateField(auto_now_add = True)
		
	# Custom Methods
	#Display something useful at interactive prompt...
	def __unicode__(self):
		return "<card> "+ str(self.sentence)
