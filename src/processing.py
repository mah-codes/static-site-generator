import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits TextNode into list of TextNodes by MD delimiter"""
    # Lane has a check for non-closed sub-sections, raising a ValueError

    
    new_nodes = []
    for node in old_nodes:
        # Only TextType.TEXT will have 'embedded' TextTypes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise ValueError("includes non-closed delimiters")
        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
        # new_nodes.extend()
    return new_nodes

def extract_markdown_images(text):
    img_regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(img_regex, text)
    return matches

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_regex, text)
    return matches