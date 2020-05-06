"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk
from langdetect import detect
from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
import os    
from TextNLPVisualiser.settings import BASE_DIR

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def segmentation(request):
    '''Renders segmentation page'''
    #assert isinstance(request, HttpRequest)
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        result = sent_tokenize(value)
        
    return render(
        request,
        'app/segmentation.html',
        {
            'title':'Contact',
            'message':'Segmentation page.',
            'year':datetime.now().year,
            'result' : result
        }
    )

def tokenize_func(value):
    '''
    Tokenize string
    '''
    result = word_tokenize(value)
    return list(filter(lambda x: x !=',' and x != '.' and x != '!' and  x != '?', result))

def tokenization(request):
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        result = tokenize_func(value)
        
    return render(
        request,
        'app/tokenization.html',
        {
            'title':'Tokenization',
            'message':'Tokenization page.',
            'year':datetime.now().year,
            'result' : result
        }
    )

def tagRussian(words):
    '''
    TAG russian words
    '''
    dir = BASE_DIR
    full_dir = os.path.join(BASE_DIR, 'app\\nltk4russian-master\\data\\media1.tab')
    with open(full_dir, encoding='utf-8') as f:
        sentenses = list(read_corpus_to_nltk(f))

    t = PMContextTagger(sentenses,type_="full")
    return t.tag(words)

def tag_func(value):
    '''
    TAG string 
    '''
    words = tokenize_func(value)

    lang = detect(value)
    if (lang == 'ru' or lang == 'mk'):
        return tagRussian(words)
    elif (lang == 'en'):
        return nltk.tag.pos_tag(words, lang='eng')
    else:
        return list({"language is not suported: {}".format(lang)})

def tagger(request):
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        result = tag_func(value)
        
    return render(
        request,
        'app/tagger.html',
        {
            'title':'POS Tagging',
            'message':'Tokenization page.',
            'year':datetime.now().year,
            'result' : result
        }
    )

from nltk import RegexpParser

def chunk(request):
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        tagged = tag_func(value)
            
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        cp  = nltk.RegexpParser(grammar)
        result = cp.parse(tagged)
        result.draw()

    return render(
        request,
        'app/chunk.html',
        {
            'title':'Chunk',
            'message':'Chunking page.',
            'year' : datetime.now().year,
            'result' : result
        }
    )

def application(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/application.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

from django.views.decorators.csrf import csrf_exempt
from syntax import syntax_analize

@csrf_exempt
def process(request):
    assert isinstance(request, HttpRequest)
    input = request.GET["val"]
    result = syntax_analize(input)  
    return JsonResponse({'result': result})  
  