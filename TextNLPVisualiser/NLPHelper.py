from nltk4russian.tagger import PMContextTagger
from nltk4russian.util import read_corpus_to_nltk
import requests
import json
import os

class NLPHelper():
    def __init__(self,base_dir):
        self.base_dir = base_dir

    def get_lemma(self,word):
        '''
        Gets lemma of word from ISPRAS API
        '''
        KEY = "e62b8387b81fe88413788ea6bd4ea45f6fdb7935"
        header = { 
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        body = [{
            "text" : word
        }]
        body = json.dumps(body)
        url = "http://api.ispras.ru/texterra/v1/nlp?targetType=lemma&apikey={}".format(KEY)
        r = requests.post(url,data=body,headers=header)
        res = json.loads(r.text)
        return res[0]["annotations"]["lemma"][0]["value"]

    def tag_russian(self, words):
        '''
        Tags russian words
        '''
        full_dir = os.path.join(self.base_dir, 'app\\nltk4russian-master\\data\\media1.tab')
        with open(full_dir, encoding='utf-8') as f:
            sentenses = list(read_corpus_to_nltk(f))

        t = PMContextTagger(sentenses,type_="full")
        return t.tag(words)

    def get_syntax_relation(self,sentense):
        '''
        Gets dependency parse as json from ISPRAS API
        '''
        KEY = "e62b8387b81fe88413788ea6bd4ea45f6fdb7935"
        header = { 
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        body = [{
            "text" : sentense
        }]
        body = json.dumps(body)
        url = "http://api.ispras.ru/texterra/v1/nlp?targetType=syntax-relation&apikey={}".format(KEY)
        r = requests.post(url,data=body,headers=header)
        return json.loads(r.text)

    def dependency_parse(self,sentense):
        '''
        Creates list of values: {value,parent,type}
        '''
        resp = self.get_syntax_relation(sentense)[0]
        annotations = resp["annotations"]["syntax-relation"]
        root_json = list(filter(lambda x: "parent" not in x["value"],annotations))[0]
        root = sentense[int(root_json["start"]):int(root_json["end"])]

        result = list()
        root_dict = {"value": root,"parent":"#","type": "root"}
        result.append(root_dict)

        for an in annotations:
            value = sentense[int(an["start"]):int(an["end"])]
            json_val = an["value"]
            if("parent" in json_val):
                json_parent = json_val["parent"]
                type = json_val["type"]
                parent = sentense[int(json_parent["start"]):int(json_parent["end"])]

                result.append({
                    "value": value,
                    "parent":parent,
                    "type": type
                })

        return result        