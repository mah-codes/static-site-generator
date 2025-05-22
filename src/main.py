from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode

def main():
    some_node = TextNode("Some anchor text", TextType.LINK, "www.google.com")
    print(some_node)

main()
