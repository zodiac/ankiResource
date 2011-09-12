from django.conf.urls.defaults import *
from django.views.generic.date_based import archive_index
from django.views.generic.list_detail import object_detail
from tagging.views import tagged_object_list
from ankiResource.cards.models import Card

urlpatterns = patterns('',
	#sentence index
	url(r'^$', archive_index, {'template_name':'cards/index.html', 'queryset':Card.objects.all(), 'date_field':'due'}, name="url_cards_index"),
	
	#show sentences as a list
	url(r'^all/$', 'ankiResource.cards.views.list', name="url_cards_list"),

	#shows a specific sentence
	#url(r'^(?P<object_id>\d+)$', object_detail, {'queryset':Sentence.objects.all()}, name="url_sentences_sentence"),
	#url(r'^(?P<sentence_id>\d+)$', 'ankiResource.sentences.views.sentence', name="url_sentences_sentence"),	
)

