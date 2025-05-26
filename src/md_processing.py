from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return [block.strip() for block in markdown.split("\n\n")]

def markdown_block_to_blocktype(md_block):
    lines = md_block.split("\n")

    if re.match(r"^#{1,6}\s\w+", md_block):
        return BlockType.HEADING
    elif re.match(r"^```\w*```$", md_block):
        return BlockType.CODE
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
        return BlockType.UNORDERED_LIST
    elif re.match(r"^\d+\.\s\w+", md_block):
        block_numbers = re.findall(r"(?m)^(\d+)\.\s.+", md_block)
        if block_numbers == [str(i) for i in range(1, len(block_numbers) + 1)]:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


# LANE's CODE, simpler and without the use of REGEX:
# Keeping here for learning purposes, but not using in the project.
def block_to_block_type_BOOTDEV(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH