from src import db

def get_total_links():
    return len(db.get_links())

def get_followed_count():
    return sum(1 for _, followed in db.get_links() if followed)

def get_unfollowed_count():
    return sum(1 for _, followed in db.get_links() if not followed)

def get_follow_back_rate():
    total = get_total_links()
    followed = get_followed_count()
    return (followed / total) * 100 if total else 0
# TODO: Add more analytics as needed (e.g., top posters if post/user info is stored) 