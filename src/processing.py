import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits TextNode into list of TextNodes by MD delimiter"""
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
    return new_nodes

def extract_markdown_images(text):
    img_regex = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(img_regex, text)
    return matches

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(link_regex, text)
    return matches

def split_nodes_link(node_list):
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    new_nodes = []
    for node in node_list:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = re.split(link_regex, node.text)
        link_tuples = extract_markdown_links(node.text)
        i = 0
        while i < len(split_nodes):
            if link_tuples != [] and split_nodes[i] == link_tuples[0][0]:
                link_text, link_url = link_tuples.pop(0)
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                i += 2 # because anchor text AND link are 2 elements split_nodes
            elif split_nodes[i] == "":
                i += 1
            else:
                new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                i += 1
    return new_nodes

def split_nodes_image(node_list):
    image_regex = r"!\[(.*?)\]\((.*?)\)"
    new_nodes = []
    for node in node_list:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = re.split(image_regex, node.text)
        image_tuples = extract_markdown_images(node.text)
        i = 0
        while i < len(split_nodes):
            if image_tuples != [] and split_nodes[i] == image_tuples[0][0]:
                image_text, image_url = image_tuples.pop(0)
                new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
                i += 2 # because anchor text AND link are 2 elements split_nodes
            elif split_nodes[i] == "":
                i += 1
            else:
                new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                i += 1
    return new_nodes

# def text_to_textnodes(text):
#     text_delimiters = {
#         "**": TextType.BOLD,
#         "_": TextType.ITALIC,
#         "`": TextType.CODE,
#     }
#     # remove links and images
    
#     for char in text:
#         if char in text_delimiters
