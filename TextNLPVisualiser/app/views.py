"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

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

from nltk.tokenize import sent_tokenize

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

from nltk.tokenize import word_tokenize

def tokenization(request):
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        result = word_tokenize(value)
        if(isinstance(result, list)):
            result = list(filter(lambda x: x !=',' and x != '.' and x != '!' and  x != '?', result))
        
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

import nltk
from langdetect import detect

def tagger(request):
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        lang = detect(value)
        words = word_tokenize(value)
        if(isinstance(words, list)):
            words = list(filter(lambda x: x !=',' and x != '.' and x != '!' and  x != '?', words))

        if (lang == 'ru'):
           result = nltk.tag.pos_tag(words, lang='rus')
        elif (lang == 'en'):
            result = nltk.tag.pos_tag(words, lang='eng')
        else:
            result = list({"language is not suported"})
        
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

from nltk import RegexpParser

def chunk(request):
    result = ''
    if request.POST.get('value'):
        value = request.POST.get('value')
        lang = detect(value)
        words = word_tokenize(value)
        if(isinstance(words, list)):
            words = list(filter(lambda x: x !=',' and x != '.' and x != '!' and  x != '?', words))

        tagged = ''
        if (lang == 'ru'):
           tagged = nltk.tag.pos_tag(words, lang='rus')
        elif (lang == 'en'):
            tagged = nltk.tag.pos_tag(words, lang='eng')
        else:
            tagged = list({"language is not suported"})
            
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
        
  