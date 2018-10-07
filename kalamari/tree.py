from .exceptions import OverrideRootError, TreeHeightError


class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []
        self.container = []

        if self.parent:
            self.parent.add_child(self)

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data

    def add_child(self, node):
        self.children.append(node)

    def add_value(self, value):
        self.container.append(value)

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def get_value(self):
        if len(self.container) == 1:
            return self.container[0]
        else:
            return self.container

class Tree:
    def __init__(self, root=None):
        self.root = root
        if self.root:
            self.tree = {0: [self.root]}
        else:
            self.tree = {}

    def __repr__(self):
        return str(self.tree)

    def __getitem__(self, level):
        return self.tree[level]

    def __iter__(self):
        for i in self.tree:
            for j in self.tree[i]:
                yield (i, j)
        
    def bfs(self):
        from collections import deque
        q = deque()
        q.append(self.root)

        while len(q) != 0:
            curr = q.popleft()
            print(curr.children)
            for i in curr.children:
                if len(i.children) > 0:
                    q.append(i)

    def add_node(self, node, level=0):
        if self.root:
            if level:
                try:
                    if level <= self.depth:
                        self.tree[level].append(node)
                    else:
                        raise TreeHeightError
                except KeyError:
                    self.tree[level] = [node]
            else:
                raise OverrideRootError
        else:
            self.root = node
            self.tree.update({0: [self.root]})

    def reveal(self):
        # do bfs
        # print tree horizontally
        #           | --   node1 -- node3
        #   root -- |
        #           | --   node2 -- node4
        #                             |
        #                             | -- node5
        #                             | -- node6
        #self.bfs()
        res = self.print_tree(self.root)
        print(res)
        # self.__iter__()
        pass

    def head(self):
        # do bfs for 1 to 3 levels, depending on self.depth
        # print tree horizontally
        #           | --   node1 -- node3
        #   root -- |
        #           | --   node2 -- node4
        #                             |
        #                             | -- node5
        #                             | -- node6
        #                             | -- node7 -- ...
        pass

    def print_tree(self, node, depth=0):
        ret = ""
        children = node.children
        midIndex = int(len(children) / 2) - 1
        top = children[:midIndex+1]
        bottom = children[midIndex+1:]

        # Print right branch
        if top != None and len(top) > 0:
            for ind, i in enumerate(top):
                if ind == 0:
                    ret += "\n"
                ret += self.print_tree(i, depth + 1)

        # Print own value
        if depth > 0:
            ret += "\n" + ("   "*depth) + "+---" + str(node.data)
        else:
            ret += "\n*" + str(node.data) 
        # print("\n" + ("    "*depth) + str(self.data))

        # Print left branch
        if bottom != None and len(bottom) > 0:
            for ind, i in enumerate(bottom):
                ret += self.print_tree(i, depth + 1)
                if ind == len(bottom) - 1:
                    ret += "\n"

        return ret

    @property
    def depth(self):
        return sum(1 for key in self.tree.keys())

    @classmethod
    def tree_from_dict(cls, json_dict):
        from collections import deque
        tree = cls()
        q = deque()
        q.append({
            'parent': Node("root"),
            'children': json_dict,
            'level': 0
                })
        while q:
            current_obj = q.popleft()
            current_parent = current_obj['parent']
            if not tree.root:
                tree.add_node(current_parent)
                current_obj['level'] += 1
            for i in current_obj['children']:
                if type(current_obj['children'][i]) == dict:
                    node_obj = Node(i, current_parent)
                    q.append({
                        'parent': node_obj,
                        'children': current_obj['children'][i],
                        'level': current_obj['level'] + 1
                            })
                    tree.add_node(node_obj, current_obj['level'])
                else:
                    node_obj = Node(i, current_parent)
                    node_obj.add_value(current_obj['children'][i])
                    tree.add_node(node_obj, current_obj['level'])
        return tree
