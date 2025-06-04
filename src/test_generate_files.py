import generate_files
import unittest
import os

class TestGenerateFiles(unittest.TestCase):
    def test_extract_title(self):
        # Get the directory where this test file is located
        test_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct path to test.md relative to the test file, including the test subdirectory
        test_file_path = os.path.join(test_dir, "test", "test.md")
        title = generate_files.extract_title(test_file_path)
        self.assertEqual(title, "Title of the test File")

if __name__ == "__main__":
    unittest.main()