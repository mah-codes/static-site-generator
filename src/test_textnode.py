import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_non_eq(self):
        node = TextNode("this is node 1", TextType.BOLD)
        node2 = TextNode("this is node 2", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_non_eq2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("this is node 1", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_url_not_none(self):
        node = TextNode("this is a link node", TextType.LINK, "www.imgur.com")
        self.assertNotEqual(node.url, None)

    def test_eq_url(self):
        node = TextNode("text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("some text node", TextType.LINK, "www.google.com")
        self.assertEqual(
            "TextNode(some text node, link, www.google.com)",
            repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode(
            "image of two cats",
            TextType.IMAGE,
            "https://www.hartz.com/wp-content/uploads/2024/03/adopting-two-cats-at-once-1.jpg"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {
            "src": "https://www.hartz.com/wp-content/uploads/2024/03/adopting-two-cats-at-once-1.jpg",
            "alt": "image of two cats"
        })
             
    def test_link(self):
        node = TextNode(
            "this be anchor text",
            TextType.LINK,
            "www.boot.dev"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "this be anchor text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, {"href": "www.boot.dev"})

    def test_italic(self):
        node = TextNode(
            "this is italic text",
            TextType.ITALIC
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "this is italic text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

if __name__ == "__main__":
    unittest.main()
