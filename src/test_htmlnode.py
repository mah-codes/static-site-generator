import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        # tag, value, children, props
        node = HTMLNode(
            "a",
            "this is anchor TEXT",
            None,
            {"href": "https://example.com"}
        )
        test_node = " href=\"https://example.com\""
        self.assertEqual(node.props_to_html(), test_node)
    
    def test_props_to_html_props(self):
        node = HTMLNode(
            "a",
            "this is anchor TEXT",
            None,
            {"href": "https://example.com", "target": "_blank"}
        )
        test_node = " href=\"https://example.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), test_node)
        
    def test_props_to_html_empty_dict(self):
        node = HTMLNode(
            "p",
            "This is plain paragraph text",
            None,
            {}
        )
        test_node = None
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_None_props(self):
        node = HTMLNode(
            "p",
            "This is plain paragraph text",
            None,
            None
        )
        test_node = None
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Follow the white rabbit",
            {'href': 'https://www.thematrix.com'}
        )
        self.assertEqual(
            node.to_html(),
            "<a href=\"https://www.thematrix.com\">Follow the white rabbit</a>"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_mult_children(self):
        child_with_children = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        children = [
            LeafNode("span", "child-span"),
            LeafNode("p", "child-p"),
            child_with_children
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child-span</span><p>child-p</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>"
        )
