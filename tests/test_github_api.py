import unittest
from unittest.mock import patch, Mock
from src import github_api

class TestGitHubAPI(unittest.TestCase):
    @patch('src.github_api.requests.get')
    def test_authenticate_github_success(self, mock_get):
        mock_get.return_value = Mock(status_code=200)
        self.assertTrue(github_api.authenticate_github('token'))

    @patch('src.github_api.requests.get')
    def test_authenticate_github_fail(self, mock_get):
        mock_get.return_value = Mock(status_code=401, text='Bad credentials')
        self.assertFalse(github_api.authenticate_github('badtoken'))

    @patch('src.github_api.requests.put')
    def test_follow_user_success(self, mock_put):
        mock_put.return_value = Mock(status_code=204)
        self.assertEqual(github_api.follow_user('testuser', 'token'), 'Success')

    @patch('src.github_api.requests.put')
    def test_follow_user_rate_limit(self, mock_put):
        mock_put.return_value = Mock(status_code=403, text='API rate limit exceeded')
        self.assertEqual(github_api.follow_user('testuser', 'token'), 'Rate limit exceeded')

    @patch('src.github_api.requests.put')
    def test_follow_user_fail(self, mock_put):
        mock_put.return_value = Mock(status_code=404, text='Not Found')
        self.assertTrue('Failed' in github_api.follow_user('testuser', 'token'))

if __name__ == "__main__":
    unittest.main() 