import requests
from bs4 import BeautifulSoup
import re

def scrape_x(username, password=None):
    # For demo: scrape public X profile page (no login)
    url = f'https://x.com/{username}'
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f"Failed to fetch X profile: {resp.status_code}")
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    posts = []
    for tweet in soup.find_all('div', {'data-testid': 'tweetText'}):
        posts.append(tweet.get_text())
    return posts

def extract_github_links_from_posts(posts):
    github_links = []
    pattern = re.compile(r'https?://github\.com/[A-Za-z0-9_-]+')
    for post in posts:
        github_links.extend(pattern.findall(post))
    return list(set(github_links)) 