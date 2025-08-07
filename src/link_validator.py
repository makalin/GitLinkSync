import requests
import re
from typing import Dict, Optional

def validate_github_link(url: str) -> bool:
    """Check if a GitHub link is valid and accessible."""
    try:
        response = requests.head(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def extract_username_from_url(url: str) -> Optional[str]:
    """Extract username from GitHub URL."""
    pattern = r'https?://github\.com/([A-Za-z0-9_-]+)'
    match = re.match(pattern, url)
    return match.group(1) if match else None

def get_user_info(username: str, token: str = None) -> Optional[Dict]:
    """Fetch GitHub user information."""
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        response = requests.get(f'https://api.github.com/users/{username}', headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def enrich_link_info(url: str, token: str = None) -> Dict:
    """Enrich link with user information."""
    info = {'url': url, 'valid': False, 'username': None, 'user_info': None}
    
    if validate_github_link(url):
        info['valid'] = True
        username = extract_username_from_url(url)
        info['username'] = username
        
        if username:
            user_info = get_user_info(username, token)
            if user_info:
                info['user_info'] = {
                    'name': user_info.get('name'),
                    'bio': user_info.get('bio'),
                    'followers': user_info.get('followers'),
                    'public_repos': user_info.get('public_repos')
                }
    
    return info
