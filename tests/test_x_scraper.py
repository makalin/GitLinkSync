import unittest
from src import x_scraper

class TestXScraper(unittest.TestCase):
    def test_scrape_x(self):
        # This test will likely fail without a real X profile and network
        self.assertIsInstance(x_scraper.scrape_x('user'), list)

    def test_extract_github_links_from_posts(self):
        posts = [
            'Check out my GitHub: https://github.com/testuser',
            'Another: https://github.com/anotheruser',
            'No link here.'
        ]
        links = x_scraper.extract_github_links_from_posts(posts)
        self.assertIn('https://github.com/testuser', links)
        self.assertIn('https://github.com/anotheruser', links)
        self.assertNotIn('No link here.', links)

if __name__ == "__main__":
    unittest.main() 