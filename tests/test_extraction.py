import unittest
import sys
import os

# Add the scripts folder to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from extract_data import extract_text_from_file  # Now it should work

class TestTikaExtraction(unittest.TestCase):
    def test_text_extraction(self):
        sample_file = "../data/raw/Brown_Inc_PO_11.txt"
        text = extract_text_from_file(sample_file)
        self.assertTrue(len(text) > 0, "Extraction failed!")

if __name__ == "__main__":
    unittest.main()
