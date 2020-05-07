from nltk import sent_tokenize
from enum import Enum
import sys
sys.path.append(".")
from NLPHelper import NLPHelper
from Tree import Tree

class ERAFinder():
    def __init__(self,base_dir):
        self.nlp_helper = NLPHelper(base_dir)
        self.results = {}
        self.base_dir = base_dir
    
    def find_entity(self, tree, main = True, banned = None):
        '''
        '''
        words = list()
        found_nodes = list()

        if(main):
            #нахождение предикатов
            if banned is None:
                tree.find_by_attr(tree, "type", "предик", found_nodes)
            else:
                tree.find_by_attr_banned(tree, "type", "предик", banned, found_nodes)
    
        else:
            types = ["1-компл","2-компл","3-компл"]

            for t in types:
                if banned is None:
                    tree.find_by_attr(tree, "type", t , found_nodes)
                else:
                    tree.find_by_attr_banned(tree, "type", t , banned, found_nodes)

        res_node = found_nodes[0]
        if len(found_nodes) > 1:
            print("More than 1 noun as entity:")
            res_node = tree.closest_to(tree, found_nodes)
            print("Closest is", res_node.value)

        words.append(res_node.value["value"])

        tagged = self.nlp_helper.tag_russian(words)
        tagged_nouns = list(filter(lambda x: TagsHelper(x).get_pos()== POSEnum.NOUN.value ,tagged))
        result_entity = {"raw": "","value":""}

        word = TagsHelper(tagged_nouns[0])

        #try to find adj 
        adj = res_node.any_child_with_attr("type","опред")
        adj_val = ""
        if (adj is not None):
            adj_val = adj.value["value"]

        result_entity["raw"] = "{}{}".format(adj_val + " ", word.word)      
        
        #приводим к нормальной форме
        if(word.get_case() != CaseEnum.NOMINATIVE.value or word.get_plur() != "sing"):
            lemma = self.nlp_helper.get_lemma(word.word)
            result_entity["value"] = lemma
        else:
            result_entity["value"] = word.word

        return result_entity

    def find_entities(self,tree,banned = None):
        '''
        Find entities for relation
        ["main"] = main entity
        ["depend"] = depend entity
        '''
        res = {"main": {} ,"depend": {} }
        res["main"] = self.find_entity(tree, True, banned)
        res["depend"] =  self.find_entity(tree, False, banned)
        return res
        
    def find_attributes(self,parsed):
        return None

    def find_relations(self,parsed,main = True):
        root = parsed[0]
        word = self.nlp_helper.tag_russian(list({root["value"]}))
        th_root = TagsHelper(word[0])
        if(th_root.get_pos() == POSEnum.VERB.value):
            print("relation", th_root.word)
            return th_root.word
        else:
            print("Root is not verb")

    def create_parse_tree(self,values,parent_tree,parent_val):
        '''
        Creates Parse-Tree
        '''
        childs = list(filter(lambda x: x["parent"] == parent_val,values))
        for c in childs:
            tree = Tree(c,parent_tree)
            parent_tree.add_child(tree)
            self.create_parse_tree(values,tree,c["value"])

    def analize(self,sentense):
        '''
        Returns json with Entities, RelationShips and Attributes
        From sentense = 'sentense'
        '''
        parsed = self.nlp_helper.dependency_parse(sentense)
        result = list()
        
        #data tree
        root = parsed[0]
        tree_root = Tree(root)
        self.create_parse_tree(parsed,tree_root,root["value"])

        #find additional relations
        #-nodes sent-soch
        sent_soch_rel = list()
        tree_root.find_by_attr(tree_root,"type","сент-соч",sent_soch_rel)

        sent_soch_dicts = list()
        for ss in sent_soch_rel:
            ss_ents = self.find_entities(ss)
            sent_soch_dicts.append({"relation" : ss.value["value"], "from":ss_ents["main"],"to":ss_ents["depend"]})

        #-nodes relat
        relat_rel = list()
        tree_root.find_by_attr(tree_root,"type","релят",relat_rel)

        relat_rel_dicts = list()
        for r in relat_rel:
            r_ents = self.find_entities(r)
            relat_rel_dicts.append({"relation" : r.value["value"], "from":r_ents["main"],"to":r_ents["depend"]})
           
        #find main realation
        banned = sent_soch_rel + relat_rel #exclude found nodes
        main_ents = self.find_entities(tree_root,banned)
        main_rel_dict = {"relation": tree_root.value["value"], "from" : main_ents["main"], "to": main_ents["depend"]}

        #for each entitiy find attributes

        result = sent_soch_dicts + relat_rel_dicts
        result.append(main_rel_dict)
        return result


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