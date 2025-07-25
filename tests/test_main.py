import unittest
from unittest.mock import patch
from src import main

class TestMain(unittest.TestCase):
    @patch('src.main.load_config')
    def test_scrape_x_posts(self, mock_config):
        mock_config.return_value = {'x_username': 'user', 'x_password': 'pass'}
        with patch('src.x_scraper.scrape_x', return_value=['post1', 'post2']):
            posts = main.scrape_x_posts()
            self.assertEqual(posts, ['post1', 'post2'])

    def test_extract_github_links(self):
        posts = ['Check https://github.com/testuser']
        with patch('src.x_scraper.extract_github_links_from_posts', return_value=['https://github.com/testuser']):
            links = main.extract_github_links(posts)
            self.assertEqual(links, ['https://github.com/testuser'])

    @patch('src.main.load_config')
    def test_follow_back_on_github(self, mock_config):
        mock_config.return_value = {'github_token': 'token'}
        with patch('src.github_api.authenticate_github', return_value=True), \
             patch('src.github_api.follow_user', return_value='Success'), \
             patch('src.db.mark_as_followed') as mock_mark:
            main.follow_back_on_github(['https://github.com/testuser'])
            mock_mark.assert_called_with('https://github.com/testuser')

if __name__ == "__main__":
    unittest.main() 