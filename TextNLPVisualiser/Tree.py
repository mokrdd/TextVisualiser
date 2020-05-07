class Tree(object):
    "Generic tree node."
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

    def any_child_with_attr(self, attr_name, attr_value):
        for ch in self.children:
            if (ch.value[attr_name] == attr_value):
                return ch

    def find_by_attr(self, node, attr_name, attr_value, result):
        if(node.value[attr_name] == attr_value):
            result.append(node)

        for ch in node.children:
            self.find_by_attr(ch,attr_name,attr_value,result)

    def find_by_attr_banned(self, node, attr_name,attr_value,banned,result):
        if(node.value[attr_name] == attr_value):
            result.append(node)

        valid_childs = list(filter(lambda x: x not in banned,node.children))
        for ch in valid_childs:
            self.find_by_attr_banned(ch,attr_name,attr_value,banned,result)

    def get_depth(self, node, current=0):
        if(node.parent == None):
            return current

        return node.get_depth(node.parent, current+1)

    def get_depth_to_node(self, to_node, node, current=0):
        if(node.parent == to_node):
            return current

        return node.get_depth(node.parent, current+1)    

    def closest_to(self, to_node, nodes):
        '''
        Finds node which is closest to node 'to_node'
        '''
        min_depth = 100000000
        min_node = None
        for n in nodes:
            depth = n.get_depth_to_node(to_node,n)
            if depth < min_depth:
                min_depth = depth
                min_node = n
        return min_node
               
