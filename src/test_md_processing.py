import unittest

from md_processing import *

class TestMarkdownBlockProcessor(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_block_to_blocktype_heading(self):
        md = "# This is a heading"
        block_type = markdown_block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_markdown_block_to_blocktype_paragraph(self):
        md = "This is a paragraph"
        block_type = markdown_block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_block_to_blocktype_ordered_list(self):
        md = "1. This is a list item\n2. This is another list item"
        block_type = markdown_block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_markdown_block_to_blocktype_ordered_list_invalid(self):
        md = "1. This is a list item\n2. This is another list item\n2. This is a third list item"
        block_type = markdown_block_to_blocktype(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_markdown_block_to_blocktype_mixed(self):
        md = """
# This is a heading

This is a paragraph

- This is a list
- with items
        """
        block_types = []
        for block in markdown_to_blocks(md):
            block_types.append(markdown_block_to_blocktype(block))
        self.assertListEqual(
            block_types,
            [
                BlockType.heading,
                BlockType.paragraph,
                BlockType.unordered_list,
            ],
        )