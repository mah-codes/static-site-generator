from textnode import *

def main():
    print("hello world")
    some_node = TextNode("Some anchor text", TextType.LINK_TEXT, "www.google.com")
    print(some_node)
main()
