from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """Splits TextNode into list of TextNodes by MD delimiter"""
    # Remember: delimiter is given already, hence always max 3 resulting nodes
    # Segregate tgt text (incl delimiter) from TextNode
    # check for delimiters within delimited text? recursion
    new_nodes = []
    for node in old_nodes:
        inner_delim_ind = node.text.find(delimiter)
        outer_delim_ind = node.text.find(delimiter, inner_delim_ind + 1)
        if inner_delim_ind < 0:
            new_nodes.append(node)
            continue
        outer_node_1 = TextNode(
            node.text[:inner_delim_ind],
            TextType.TEXT,
            url=None
        )
        inner_node = TextNode(
            node.text[inner_delim_ind + 1:outer_delim_ind],
            text_type,
            url=None
        )
        outer_node_2 = TextNode(
            node.text[outer_delim_ind + 1:],
            TextType.TEXT,
            url=None
        )
        new_nodes.extend([outer_node_1, inner_node, outer_node_2])
    return new_nodes
