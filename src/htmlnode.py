
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
        props_html = " ".join(list(map(lambda k: f"{k}=\"{self.props[k]}\"", self.props)))
        return " " + props_html
        
    def __repr__(self):
        return f"""HTMLNode:
            tag: {self.tag}
            value: {self.value}
            children: {self.children}
            props: {self.props}
        """

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
 
    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value
        node_props = self.props_to_html()
        return f"<{self.tag}{node_props}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Node needs a tag")
        if self.children == None or self.children == []:
            raise ValueError("Parent Tag requires children")
        props_html = self.props_to_html()
        
        nested_children = any(list(map(lambda item: isinstance(item, list), self.children)))
        if not nested_children:
            html_children = "".join(list(map(lambda child: child.to_html(), self.children)))
            return f"<{self.tag}{props_html}>{html_children}</{self.tag}>"
        if nested_children:
            output = []
            for child in self.children:
                if isinstance(child, list):
                    output.append(child.to_html())
            return output

            
