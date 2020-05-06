import requests
import json
from nltk import sent_tokenize

def get_syntax_relation(sentence):
    KEY = "e62b8387b81fe88413788ea6bd4ea45f6fdb7935"
    header = { 
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    body = [{
        "text" : sentence
    }]
    body = json.dumps(body)
    url = "http://api.ispras.ru/texterra/v1/nlp?targetType=syntax-relation&apikey={}".format(KEY)
    r = requests.post(url,data=body,headers=header)
    
    return json.loads(r.text)

def printTree(values,parent_val):
    childs = list(filter(lambda x: x["parent"] == parent_val,values))
    for c in childs:
        print(c)
        printTree(values,c["value"])

def syntax_analize(text):
    res = list()
    sents = sent_tokenize(text)

    for sentence in sents:
        resp = get_syntax_relation(sentence)[0]
        annotations = resp["annotations"]["syntax-relation"]
        root_json = list(filter(lambda x: "parent" not in x["value"],annotations))[0]
        root = sentence[int(root_json["start"]):int(root_json["end"])]
        result = list()
        result.append({
            "value": root,
            "parent": "#",
            "type": ""
            })

        result_4_js = list()
        result_4_js.append({
            "id": root,
            "parent": "#",
            "text": root
        })

        for an in annotations:
            value = sentence[int(an["start"]):int(an["end"])]
            json_val = an["value"]
            if("parent" in json_val):
                json_parent = json_val["parent"]
                type = json_val["type"]
                parent = sentence[int(json_parent["start"]):int(json_parent["end"])]
                result.append({
                    "value":value,
                    "parent":parent,
                    "type": type
                })

                result_4_js.append({
                    "id": value,
                    "parent": parent,
                    "text": "{}/{}".format(value,type)
                })
            
        res.append(result_4_js)

    return res

def analize_sentence(tree):
    root = tree.pop(filter(lambda x: x["parent"]=="#",tree))
    first_nodes = list(filter(lambda x: x["parent"] == root,tree))

def syntax_analize_finale(text):
    res = list()
    sents = sent_tokenize(text)

    for sentence in sents:
        resp = get_syntax_relation(sentence)[0]
        annotations = resp["annotations"]["syntax-relation"]
        print(annotations)
        root_json = list(filter(lambda x: "parent" not in x["value"],annotations))[0]
        root = sentence[int(root_json["start"]):int(root_json["end"])]

        result = list()
        result.append({
            "value": root,
            "parent": "#",
            "type": ""
            })

        result_4_js = list()
        result_4_js.append({
            "id": root,
            "parent": "#",
            "text": root
        })

        for an in annotations:
            value = sentence[int(an["start"]):int(an["end"])]
            json_val = an["value"]
            if("parent" in json_val):
                json_parent = json_val["parent"]
                type = json_val["type"]
                parent = sentence[int(json_parent["start"]):int(json_parent["end"])]
                result.append({
                    "value":value,
                    "parent":parent,
                    "type": type
                })

                result_4_js.append({
                    "id": value,
                    "parent": parent,
                    "text": "{}/{}".format(value,type)
                })
         
        analize_sentence(result)
                
        res.append(result_4_js)

    return res