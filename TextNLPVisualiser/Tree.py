class Tree(object):
    def __init__(self, value, parent = None, children=None):
        self.value = value
        self.parent = parent
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.value

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

    def find_by_attr(self, node, attr_name, attr_value, result):
        '''
        Finds all nodes where node.value[attr_name] = attr_value
        '''
        if(node.value[attr_name] == attr_value):
            result.append(node)

        for ch in node.children:
            self.find_by_attr(ch,attr_name,attr_value,result)

    def find_by_attr_banned(self, node, attr_name,attr_value,banned,result):
        '''
        Finds all nodes where node.value[attr_name] = attr_value
            excluding subtrees with root at 'banned' 
        '''
        if(node.value[attr_name] == attr_value):
            result.append(node)

        valid_childs = list(filter(lambda x: x not in banned, node.children))
        for ch in valid_childs:
            self.find_by_attr_banned(ch,attr_name,attr_value,banned,result)

    def get_depth(self, node, current=0):
        if(self.parent == None):
            return current
        self.get_depth(self, self.parent, current+1)    
