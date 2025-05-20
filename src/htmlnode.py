
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # html tag
        self.value = value # text
        self.children = children # list
        self.props = props # dict

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        return " ".join(list(map(lambda k: f"{k}=\"{self.props[k]}\"", self.props)))
        
    def __repr__(self):
        return f"""HTMLNode:
            tag: {self.tag}
            value: {self.value}
            children: {self.children}
            props: {self.props}
        """

class LeafNode(HTMLNode):
    def __init__(self, tag, value, children=None, props=None):
        super().__init__(tag, value, children, props)
 
    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return value
        node_props = self.props_to_html()
        if node_props != "":
            node_props = " " + node_props

        return f"<{self.tag}{node_props}>{self.value}</{self.tag}>"
