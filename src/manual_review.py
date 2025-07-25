from src import db

def review_links():
    links = db.get_links()
    for url, followed in links:
        if not followed:
            resp = input(f"Approve follow for {url}? (y/n): ")
            if resp.lower() == 'y':
                db.mark_as_followed(url)
                print(f"Approved: {url}")
            else:
                print(f"Rejected: {url}")

if __name__ == "__main__":
    review_links() 