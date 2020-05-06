from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
from nltk.tokenize import word_tokenize

def tagRussian(value):
    with open('../data/media1.tab', encoding='utf-8') as f:
        sentenses = list(read_corpus_to_nltk(f))

    result = word_tokenize(value)

    if(isinstance(result, list)):
        result = list(filter(lambda x: x !=',' and x != '.' and x != '!' and  x != '?', result))

    t = PMContextTagger(sentenses,type_="full")

    return t.tag(result)
      



