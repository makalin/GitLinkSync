import unittest
from unittest.mock import patch, Mock
import tempfile
import os
from src import rate_limiter, link_validator, multi_account, data_cleaner, backup_manager, performance_monitor, error_handler

class TestRateLimiter(unittest.TestCase):
    def test_rate_limiter(self):
        limiter = rate_limiter.RateLimiter(max_requests=2, time_window=1)
        self.assertTrue(limiter.can_make_request())
        limiter.record_request()
        self.assertTrue(limiter.can_make_request())
        limiter.record_request()
        self.assertFalse(limiter.can_make_request())

class TestLinkValidator(unittest.TestCase):
    @patch('src.link_validator.requests.head')
    def test_validate_github_link_valid(self, mock_head):
        mock_head.return_value = Mock(status_code=200)
        self.assertTrue(link_validator.validate_github_link('https://github.com/testuser'))

    @patch('src.link_validator.requests.head')
    def test_validate_github_link_invalid(self, mock_head):
        mock_head.return_value = Mock(status_code=404)
        self.assertFalse(link_validator.validate_github_link('https://github.com/nonexistent'))

    def test_extract_username_from_url(self):
        username = link_validator.extract_username_from_url('https://github.com/testuser')
        self.assertEqual(username, 'testuser')

class TestMultiAccount(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write('{"github": [], "x": []}')
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_add_github_account(self):
        manager = multi_account.AccountManager(self.temp_file.name)
        manager.add_github_account('token123', 'user123')
        self.assertEqual(len(manager.accounts['github']), 1)

    def test_add_x_account(self):
        manager = multi_account.AccountManager(self.temp_file.name)
        manager.add_x_account('user123', 'pass123')
        self.assertEqual(len(manager.accounts['x']), 1)

class TestDataCleaner(unittest.TestCase):
    def test_normalize_github_url(self):
        normalized = data_cleaner.DataCleaner.normalize_github_url('http://github.com/testuser/')
        self.assertEqual(normalized, 'https://github.com/testuser')

    def test_remove_duplicates(self):
        links = ['https://github.com/user1', 'https://github.com/user1/', 'https://github.com/user2']
        unique = data_cleaner.DataCleaner.remove_duplicates(links)
        self.assertEqual(len(unique), 2)

    def test_filter_valid_github_links(self):
        links = ['https://github.com/user1', 'https://invalid.com/user2', 'https://github.com/user3']
        valid = data_cleaner.DataCleaner.filter_valid_github_links(links)
        self.assertEqual(len(valid), 2)

class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.backup_mgr = backup_manager.BackupManager(self.temp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_create_backup(self):
        # Create a test file
        test_file = os.path.join(self.temp_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test content')
        
        backup_path = self.backup_mgr.create_backup([test_file])
        self.assertTrue(os.path.exists(backup_path))

    def test_list_backups(self):
        backups = self.backup_mgr.list_backups()
        self.assertIsInstance(backups, list)

class TestPerformanceMonitor(unittest.TestCase):
    def test_performance_monitor(self):
        monitor = performance_monitor.PerformanceMonitor()
        monitor.start_timer('test_op')
        monitor.end_timer('test_op')
        
        stats = monitor.get_operation_stats('test_op')
        self.assertIn('count', stats)
        self.assertEqual(stats['count'], 1)

    def test_api_stats(self):
        monitor = performance_monitor.PerformanceMonitor()
        monitor.record_api_call('github_api', True)
        monitor.record_api_call('github_api', False)
        
        stats = monitor.get_api_stats()
        self.assertEqual(stats['calls_by_api']['github_api'], 2)
        self.assertEqual(stats['errors_by_api']['github_api'], 1)

class TestErrorHandler(unittest.TestCase):
    def test_error_handler(self):
        handler = error_handler.ErrorHandler()
        
        # Test error handling
        try:
            raise ValueError("Test error")
        except Exception as e:
            result = handler.handle_error(e, "test_context")
            self.assertIsNone(result)

    def test_error_summary(self):
        handler = error_handler.ErrorHandler()
        
        try:
            raise ValueError("Test error")
        except Exception as e:
            handler.handle_error(e, "test_context")
        
        summary = handler.get_error_summary()
        self.assertEqual(summary['total_errors'], 1)
        self.assertEqual(summary['most_common_error'], 'ValueError')

if __name__ == "__main__":
    unittest.main()
