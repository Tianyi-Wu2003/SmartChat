import unittest
from src import wikipage

class TestWikipage(unittest.TestCase):
    def test_get_text_valid_page(self):
        # Test getting text from a valid page
        page = wikipage.Wikipage("Python (programming language)")
        page.get_text()

        # Check that the page exists and has sections
        self.assertTrue(page.found_page)
        self.assertTrue(page.sections)
        self.assertIn("History", page.text_dict)

    def test_get_text_invalid_page(self):
        # Test getting text from an invalid page
        page = wikipage.Wikipage("NonExistentPage123")
        page.get_text()

        # Check that the page does not exist
        self.assertFalse(page.found_page)
        self.assertEqual(0, len(page.text_dict))

    def test_remove_extra(self):
        # Test removing extra sections from the dictionary
        page = wikipage.Wikipage("Python (programming language)")
        page.get_text()
        page.remove_extra()

        # Check that specified sections are not in the dictionary
        self.assertNotIn('See also', page.text_dict)
        self.assertNotIn('References', page.text_dict)
        self.assertNotIn('Bibliography', page.text_dict)
        self.assertNotIn('External links', page.text_dict)


if __name__ == "__main__":
    unittest.main()
