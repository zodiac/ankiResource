from haystack import indexes
from ankiResource.sentences.models import Sentence

class SentenceIndex(indexes.SearchIndex, indexes.Indexable):
       text = indexes.CharField(document=True, use_template=True)
       sentence = indexes.CharField(model_attr='sentence')
       
       def get_model(self):
          return Sentence
