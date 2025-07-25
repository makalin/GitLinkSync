import unittest
from src import db

class TestDB(unittest.TestCase):
    def setUp(self):
        db.init_db()
        # Clean up for test
        import os
        if os.path.exists('links.db'):
            import sqlite3
            conn = sqlite3.connect('links.db')
            c = conn.cursor()
            c.execute('DELETE FROM links')
            conn.commit()
            conn.close()

    def test_init_db(self):
        # Should not raise
        db.init_db()

    def test_save_and_get_links(self):
        db.save_link('https://github.com/testuser')
        links = db.get_links()
        self.assertTrue(any('https://github.com/testuser' in l for l in [link[0] for link in links]))

    def test_mark_as_followed(self):
        db.save_link('https://github.com/testuser')
        db.mark_as_followed('https://github.com/testuser')
        links = db.get_links()
        for url, followed in links:
            if url == 'https://github.com/testuser':
                self.assertEqual(followed, 1)

if __name__ == "__main__":
    unittest.main() 