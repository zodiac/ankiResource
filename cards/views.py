from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from ankiResource import settings, accounts, media, lists
from ankiResource.cards.models import Card

def list(request):

	# Get page to render
	if 'page' in request.GET:
		page = request.GET['page']
	
	# If no page is specified, just display page 1
	else:
		page = 1
	
	#Get all sentences
	card_list = Card.objects.all().order_by('-due')
	
	# Paginate
	card_paginator = Paginator(card_list, settings.ANKIRESOURCE_ITEMS_PER_PAGE)
	card_page = card_paginator.page(page)
	
		
	#Send it all to template renderer
	dic = {
		'card_paginator': card_paginator,
	}
	
	#Render the page
	return render_to_response("cards/list.html", dic, context_instance=RequestContext(request))
