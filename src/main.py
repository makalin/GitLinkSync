import json
from src import x_scraper, db, github_api

def load_config():
    with open('config.json') as f:
        return json.load(f)

def scrape_x_posts():
    config = load_config()
    posts = x_scraper.scrape_x(config['x_username'], config['x_password'])
    return posts

def extract_github_links(posts):
    links = x_scraper.extract_github_links_from_posts(posts)
    return links

def follow_back_on_github(links):
    config = load_config()
    token = config['github_token']
    github_api.authenticate_github(token)
    for link in links:
        username = link.rstrip('/').split('/')[-1]
        result = github_api.follow_user(username, token)
        print(f'Followed {username}: {result}')
        if result == 'Success':
            db.mark_as_followed(link)

def main():
    db.init_db()
    posts = scrape_x_posts()
    links = extract_github_links(posts)
    for link in links:
        db.save_link(link)
    config = load_config()
    if config.get('auto_follow', False):
        follow_back_on_github(links)
    print(f"Extracted links: {links}")

if __name__ == "__main__":
    main() 