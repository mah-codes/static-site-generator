from enum import Enum
import re

class BlockType(Enum):
    paragraph = "paragraph"
    heading = "heading"
    code = "code"
    quote = "quote"
    unordered_list = "unordered_list"
    ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n")]

def markdown_block_to_blocktype(md_block):
    if re.match(r"^#{1,6}\s\w+", md_block):
        return BlockType.heading
    elif re.match(r"^```\w*```$", md_block):
        return BlockType.code
    elif re.match(r"^>\s\w+", md_block):
        return BlockType.quote
    elif re.match(r"^-+\s\w+", md_block):
        return BlockType.unordered_list
    elif re.match(r"^\d+\.\s\w+", md_block):
        block_numbers = re.findall(r"(?m)^(\d+)\.\s.+", md_block)
        if block_numbers == [str(i) for i in range(1, len(block_numbers) + 1)]:
            return BlockType.ordered_list
    return BlockType.paragraph
