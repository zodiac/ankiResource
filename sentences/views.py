from django.shortcuts import *
from django.http import *
from django.core.urlresolvers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User

from ankiResource import settings
from ankiResource.uploading.functions import *
from ankiResource import sentences, accounts, media
from ankiResource.sentences.forms import SentenceForm

# Create your views here.

# -----------------------------INDEX------------------------------------
# Shows the sentence index page
def index(request):
	#Get the latest 5 sentences to show on the main page
	latest_sentences_list = sentences.models.Sentence.objects.all().order_by('-pub_date')[:settings.ANKIRESOURCE_SENTENCES_INDEX_SENTENCE_NUM]
	
	dic = {
		'latest_sentences_list': latest_sentences_list,
	}
	
	return render_to_response("sentences/index.html", dic, context_instance=RequestContext(request))
	
# ----------------------------- LIST SENTENCES -------------------------
# Shows a list of sentences
def list(request):
	#Get all sentences
	sentence_list = sentences.models.Sentence.objects.all().order_by('-pub_date')
	
	#Send it all to template renderer
	dic = {
		'sentence_list': sentence_list,
	}
	
	#Render the page
	return render_to_response("sentences/list.html", dic, context_instance=RequestContext(request))

# ----------------------------- SENTENCE -------------------------------
# Shows an individual sentence.
def sentence(request, sentence_id):
	try:
		sentence = sentences.models.Sentence.objects.get(pk=sentence_id)
	except:
		raise Http404
	
	dic = {
		'sentence': sentence,
		
	}
	
	return render_to_response("sentences/sentence.html", dic, context_instance=RequestContext(request))


# ---------------------------- NEW SENTENCE ----------------------------
@login_required
# Makes a new Sentence
def new(request):
	if request.method == "POST":
		#validate the data
		form = SentenceForm(request.POST)
		
		#continue if the form is valid
		if form.is_valid():
			#Try to make the new sentence
			newSentence = sentences.models.Sentence(
													sentence=request.POST['sentence'], 
													pub_date=datetime.datetime.now(), 
													user_id=accounts.models.Profile.objects.get(pk=request.user.id).id,
													)
			
			#Right we should be good to save now =D
			#newSentence.save()
			
			#Tags
			if request.POST['tags'] != "":
				newSentence.tags = request.POST['tags']
			
			#If there is media, save it
			if 'video' in request.FILES:
				newSentence.media_set.add(sentences.models.Media(file=storeFile(request.FILES['video'], "media/video"), type="Video", sentence=newSentence))
				
			if 'sound' in request.FILES:
				newSentence.media_set.add(sentences.models.Media(file=storeFile(request.FILES['sound'], "media/sound"), type="Sound", sentence=newSentence))
				
			if 'image' in request.FILES:
				newSentence.media_set.add(sentences.models.Media(image=storeFile(request.FILES['image'], "media/images"), type="Image", sentence=newSentence))
				
			#Pick a language
			if request.POST['language'] == "Other" and request.POST['other_language'] != "":
				newSentence.language = request.POST['other_language']
			elif request.POST['language'] != "Other":
				newSentence.language = request.POST['language']
				
			#Now save again
			#newSentence.save()

			# Add the sentence
			id = addSentence(request, form)
			
			#Redirect the user to the new sentence.
			return HttpResponseRedirect(reverse('ankiResource.sentences.views.sentence', args=(id,)))
			
		#add the form to the dic
		dic = {'form': form}
	
		#render the page
		return render_to_response("sentences/new.html", dic, context_instance=RequestContext(request))
	
	#If we aren't already adding, draw a blank form.
	else:
		form = SentenceForm()
		
		#make a dic to hold the form
		dic = {'form': form}
		
		#render the page
		return render_to_response("sentences/new.html", dic, context_instance=RequestContext(request))


# --------------------------- DELETE SENTENCE --------------------------
@login_required
# Deletes a sentence
def delete(request, sentence_id):
	# First grab the sentence.
	sentence = sentences.models.Sentence.objects.get(pk=sentence_id)
	
	# Make a dic for the template to use.
	dic = {
	}
	
	# Only delete the sentence if the user is a superuser (admin
	# Or if the sentence is owned by them.
	if request.user == sentence.profile.user or request.user.is_superuser == True:
		# Delete the sentence.
		sentence.delete()
		
		# Tell the template the sentence was deleted
		dic.update({'deleted': True})
		
	# Tell the template access was denied
	else:
		dic.update({'deleted': False})
	
	# Render the page
	return render_to_response("sentences/del.html", dic, context_instance=RequestContext(request))
	
# ------------------------------- SHOW LIST ----------------------------
def show_list(request, list_id):
	# Make a dic
	dic = {
	}
	
	# Grab the list
	try:
		list = sentences.models.List.objects.get(pk=list_id)
	except:
		raise Http404
		
	# Put it into the dict
	dic.update({ 'list': list })
	
	# Render the template
	return render_to_response("sentences/show_list.html", dic, context_instance=RequestContext(request))

# //////////////////////////////////////////////////////////////////////
# ------------------------------- AJAX ---------------------------------
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# ---------------------------- ADD / REMOVE TO LIST --------------------
@login_required
def ajax_list_edit(request):
	print request.POST['list']
	print request.POST['sentence']
	
	# Make sure the list and sentence exist
	list = sentences.models.List.objects.get(pk=request.POST['list'])
	sentence = sentences.models.Sentence.objects.get(pk=request.POST['sentence'])
	
	print sentence.sentence
	
	# Make a dic
	dic = {
	}
	
	# K, now check if the user has permissions to do this.
	if request.user in list.user.all() or list.open:
		# Add / Remove the sentence to the list
		if 'add' in request.POST:
			if request.POST['add'] == "1":
				list.sentence.add(sentence)
				
				# Tell the template we succeeded
				dic.update({'success': True})
		
		if 'remove' in request.POST:
			if request.POST['remove'] == "1":
				list.sentence.remove(sentence)
				
				# Tell the template we succeeded
				dic.update({'success': True})
		
		# Check whether or not the sentence is in the list.
		if 'exists' in request.POST:
			if request.POST['exists'] == "1":
				if sentence in list.sentence.all():
					dic.update({'success': True})
				else:
					# Tell the template we failed
					dic.update({'success': False})
				
			
		# Save the list
		list.save()
		
	else:
		
		# Tell the template we failed =(
		dic.update({'success': False})
	
	#Render to template
	return render_to_response("sentences/ajax/list_edit.html", dic, context_instance=RequestContext(request))
