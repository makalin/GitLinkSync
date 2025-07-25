import json
from src import db, github_api

def load_config():
    with open('config.json') as f:
        return json.load(f)

def main():
    config = load_config()
    token = config['github_token']
    github_api.authenticate_github(token)
    links = db.get_links()
    for url, followed in links:
        if not followed:
            username = url.rstrip('/').split('/')[-1]
            result = github_api.follow_user(username, token)
            print(f'Followed {username}: {result}')
            if result == 'Success':
                db.mark_as_followed(url)

if __name__ == "__main__":
    main() 