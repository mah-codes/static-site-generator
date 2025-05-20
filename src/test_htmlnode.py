import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_basic(self):
        # tag, value, children, props
        node = HTMLNode(
            "a",
            "this is anchor TEXT",
            None,
            {"href": "https://example.com"}
        )
        test_node = "href=\"https://example.com\""
        self.assertEqual(node.props_to_html(), test_node)
    
    def test_props_to_html_props(self):
        node = HTMLNode(
            "a",
            "this is anchor TEXT",
            None,
            {"href": "https://example.com", "target": "_blank"}
        )
        test_node = "href=\"https://example.com\" target=\"_blank\""
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
            None,
            {'href': 'https://www.thematrix.com'}
        )
        self.assertEqual(
            node.to_html(),
            "<a href=\"https://www.thematrix.com\">Follow the white rabbit</a>"
        )

