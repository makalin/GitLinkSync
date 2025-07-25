import requests

def authenticate_github(token):
    # For this implementation, just check if the token is valid by hitting the user endpoint
    headers = {'Authorization': f'token {token}'}
    resp = requests.get('https://api.github.com/user', headers=headers)
    if resp.status_code == 200:
        print('GitHub authentication successful.')
        return True
    else:
        print(f'GitHub authentication failed: {resp.status_code} {resp.text}')
        return False

def follow_user(username, token):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github+json',
    }
    url = f'https://api.github.com/user/following/{username}'
    resp = requests.put(url, headers=headers)
    if resp.status_code == 204:
        return 'Success'
    elif resp.status_code == 403 and 'rate limit' in resp.text.lower():
        return 'Rate limit exceeded'
    else:
        return f'Failed: {resp.status_code} {resp.text}' 