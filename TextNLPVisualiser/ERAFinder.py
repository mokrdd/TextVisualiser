from nltk import sent_tokenize
from anytree import Node, RenderTree
from anytree import findall,findall_by_attr
from enum import Enum
import sys
sys.path.append(".")
from NLPHelper import NLPHelper
from Tree import Tree

class ERAFinder():
    '''
    Class for Entities, RelationShips and Attributes finding
    '''
    def __init__(self):
        self.nlp_helper = NLPHelper()
    
    def find_entity(self, parsed, main = True):
        if(main):
            type_ = 'предик'
            #нахождение предикатов
            predics = list(filter(lambda x: x["type"] == "предик", parsed))
            words = list()
            for pred in predics:
                words.append(pred["value"])

            tagged = self.nlp_helper.tag_russian(words)
            tagged_nouns = list(filter(lambda x: TagsHelper(x).get_pos()== POSEnum.NOUN.value ,tagged))
            result_entity = {"raw": "","value":"", "type":"main"}
            if len(tagged_nouns)==1:
                word = TagsHelper(tagged_nouns[0])
                result_entity["raw"] = word.word
                #приводим к нормальной форме
                if(word.get_case() != CaseEnum.NOMINATIVE.value or word.get_plur() != "sing"):
                    lemma = self.nlp_helper.get_lemma(word.word)
                    result_entity["value"] = lemma
                else:
                    result_entity["value"] = word.word
                return result_entity    
        else:
            types = ["1-компл","2-компл","3-компл"]
            compls = list(filter(lambda x: x["type"] in types, parsed))
            words = list()
            for c in compls:
                words.append(c["value"])

            tagged = self.nlp_helper.tag_russian(words)
            tagged_nouns = list(filter(lambda x: TagsHelper(x).get_pos()== POSEnum.NOUN.value ,tagged))
            result_entity = {"raw": "","value":"", "type":"depend"}
            if len(tagged_nouns)==1:
                word = TagsHelper(tagged_nouns[0])
                result_entity["raw"] = word.word
                #приводим к нормальной форме
                if(word.get_case() != CaseEnum.NOMINATIVE.value or word.get_plur() != "sing"):
                    lemma = self.nlp_helper.get_lemma(word.word)
                    result_entity["value"] = lemma
                else:
                    result_entity["value"] = word.word
                return result_entity

    def find_entities(self,parsed):
        local_list = parsed.copy()

        root_node = list(filter(lambda x: x["parent"]=="#",local_list))[0]
        local_list.remove(root_node)

        main_ent = self.find_entity(parsed, True)
        print(main_ent)

        depend_ent = self.find_entity(parsed, False)
        print(depend_ent)
        
    def find_attributes(self,parsed):
        return None

    def find_relations(self,parsed):
        root = parsed[0]
        word = self.nlp_helper.tag_russian(list({root["value"]}))
        th_root = TagsHelper(word[0])
        if(th_root.get_pos() == POSEnum.VERB.value):
            print("relation", th_root.word)
            return th_root.word
        else:
            print("Root is not verb")

    def create_parse_tree(self,values,parent_tree,parent_val):
        childs = list(filter(lambda x: x["parent"] == parent_val,values))
        for c in childs:
            tree = Tree(c,parent_tree)
            parent_tree.add_child(tree)
            self.create_parse_tree(values,tree,c["value"])

    def show_parse_tree(self,parsed):
        '''
        Builds parse-tree
        '''
        root = parsed[0]
        t = TreeHelper(parsed,root,root["value"])
        tree_root = Tree(root)
        self.create_parse_tree(parsed,tree_root,root["value"])

        # Найти все узлы sent-soch
        sent_soch = list()
        tree_root.find_by_attr(tree_root,"type","сент-соч",sent_soch)
        for r in sent_soch:
            print("сент-соч",r.value)
        # 

        # Найти все узлы relat
        relat = list()
        tree_root.find_by_attr(tree_root,"type","релят",relat)
        for r in relat:
            print("релят",r.value)
        #

        banned = sent_soch+relat
        final_res = list()
        tree_root.find_by_attr_banned(tree_root,"type","предик",banned,final_res)
        for r in final_res:
            print("предик финалОЧКА",r.value)   

        for pre, fill, node in RenderTree(t.root):
            #pass
            print("%s%s" % (pre, node.name))

    def analize(self,sentense):
        '''
        Returns json with Entities, RelationShips and Attributes
        From sentense = 'sentense'
        '''
        parsed = self.nlp_helper.dependency_parse(sentense)
        self.show_parse_tree(parsed)
        entities = self.find_entities(parsed)
        #attributes = self.find_attributes(parsed)
        relations = self.find_relations(parsed)


class TreeHelper():
    def __init__(self, values, root_dict, parent_val):
        self.root = Node(root_dict)
        self.values = values
        self.create_tree(values,self.root,parent_val)

    def create_tree(self,values,parent_node,parent_val):
        '''
        Create a tree
        'values' - list of values like {value,parent,type}
        'parent_node' - parent as Node()
        'parent_value' - value of parent["value"]
        '''
        childs = list(filter(lambda x: x["parent"] == parent_val,values))
        for c in childs:
            node = Node(c,parent_node)
            self.create_tree(values,node,c["value"])

    

class TagsHelper():
    def __init__(self,tagged_word):
        self.word = tagged_word[0]
        self.tags = tagged_word[1].split(',')

    def filter(self,filter_):
        return list(filter(filter_,self.tags))

    def get_pos(self):
        return self.filter(lambda x: x.isupper())[0]
        #return list(filter(lambda x: x.isupper(),self.tags))[0]

    def get_amin(self):
        return self.filter(lambda x: x in ["anim","inan"])[0]

    def get_plur(self):
        return self.filter(lambda x: x in ["plur","sing"])[0]

    def get_gender(self):
        return self.filter(lambda x: x in ["masc","femn","neut"])[0]

    def get_case(self):
        '''
        todo: add cases
        nomn = именительный
        gent = родительный
        datv = дательный
        accs = винительный
        ablt = творит-ый
        loct = предл-ый
        '''
        return self.filter(lambda x: x in ["nomn","gent","datv","accs","ablt","loct"])[0]

    def check(self):
        print(self.get_pos())
        print(self.get_amin())
        print(self.get_plur())
        print(self.get_gender())
        print(self.get_case())    

class CaseEnum(Enum):
    '''
    Падежи
    '''
    #именительный
    NOMINATIVE = "nomn"
    GENITIVE = "gent"
    DATIVE = "datv"
    ACCUSATIVE = "accs"
    INSTRUMENTAL = "ablt"
    PREPOSITIONAL = "loct"

class POSEnum(Enum):
    '''
    Части речи
    '''
    NOUN = "NOUN"
    VERB = "VERB"