import unittest

from textnode import TextNode, TextType


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
        node = TextNode("This is a text node", TextType.NORMAL)
        node2 = TextNode("This is a text node2", TextType.NORMAL)
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

if __name__ == "__main__":
    unittest.main()
