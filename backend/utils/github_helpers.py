# FILE: github_utils.py
import requests

def github_user_exists(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    return response.status_code == 200