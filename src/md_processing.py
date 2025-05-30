from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from text_processing import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE_BLOCK = "code_block"  # Changed from CODE to CODE_BLOCK for clarity
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    """Splits markdown into a list of blocks, removes whitespace and empty blocks"""
    md_blocks = [block.strip() for block in markdown.split("\n\n")]
    return list(filter(None, md_blocks))

def markdown_block_to_blocktype(md_block):
    lines = md_block.split("\n")

    if re.match(r"^#{1,6}\s\w+", md_block):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE_BLOCK
    elif re.match(r"^>\s\w+", md_block):
        # Making more robust (after submission)
        for line in lines:
            if line.startswith(">"):
                return BlockType.QUOTE
        return BlockType.PARAGRAPH
    elif re.match(r"^-+\s\w+", md_block):
        for line in lines:
            if line.startswith("- "):
                return BlockType.UNORDERED_LIST
        return BlockType.PARAGRAPH
    elif re.match(r"^\d+\.\s\w+", md_block):
        block_numbers = re.findall(r"(?m)^(\d+)\.\s.+", md_block)
        if block_numbers == [str(i) for i in range(1, len(block_numbers) + 1)]:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    # For loop will only convert block-to-block, not fixed for nesting
    for block in md_blocks:
        block_type = markdown_block_to_blocktype(block)
        match block_type:
            case BlockType.HEADING:
                html_nodes.append(md_block_to_heading_html_node(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(md_block_to_paragraph_html_node(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(md_block_to_ordered_list_html_node(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(md_block_to_unordered_list_html_node(block))
            case BlockType.CODE_BLOCK:
                html_nodes.append(md_block_to_code_block_html_node(block))
            case BlockType.QUOTE:
                html_nodes.append(HTMLNode(tag="blockquote", value=block))
            case _:
                raise ValueError(f"Invalid block type: {block_type}")
    return ParentNode("div", html_nodes)

def md_block_to_ordered_list_html_node(markdown_block):
    lines = markdown_block.split("\n")
    li_nodes = [] # li = list item from HTML's <li>
    for line in lines:
        # ex: 2. Second item of list
        ol_regex = r"^\d+.\s"
        ol_num_len = len(re.match(ol_regex, line).group())
        # take after "1. " or "13. " dynamically
        children = text_to_html_node_children(line[ol_num_len:])
        # should have received [LeafNode()] of this line
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ol", li_nodes)

def md_block_to_unordered_list_html_node(markdown_block):
    lines = markdown_block.split("\n")
    li_nodes = []
    for line in lines:
        children = text_to_html_node_children(line[2:])
        li_nodes.append(ParentNode("li", children))
    return ParentNode("ul", li_nodes)

def md_block_to_paragraph_html_node(markdown_block):
    lines = markdown_block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_html_node_children(paragraph)
    return ParentNode("p", children)

def md_block_to_heading_html_node(markdown_block):
    lines = markdown_block.split("\n")
    for line in lines:
        h_regex = r"^#{1,6}"
        h_level = len(re.match(h_regex, line).group())
        h_tag = f"h{h_level}"
        children = text_to_html_node_children(line[h_level + 1:])
        return ParentNode(h_tag, children)

def md_block_to_code_block_html_node(markdown_block):
    # Remove the ``` markers and join the content
    lines = markdown_block.split("\n")
    content = "\n".join(lines[1:-1])
    return ParentNode("pre",[LeafNode("code", content)])

def text_to_html_node_children(text):
    """Takes raw one-line text, transforms to text nodes then to list of HTML nodes"""
    children_nodes = []
    # remember, text nodes TextNode(TextType.TEXT, text-value) 
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        # html_nodes are leafnodes with individual tags, 'inner' values[, props]
        children_nodes.append(text_node_to_html_node(text_node))
    return children_nodes

def markdown_to_html(markdown):
    html_nodes = markdown_to_html_node(markdown)
    return "\n".join([node.to_html() for node in html_nodes])

