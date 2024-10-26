import os
import requests
import csv

GITHUB_TOKEN = "top_secret_token_do_not_touch"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# --- Step 1: Fetch Users from Moscow with over 50 followers ---
def fetch_users_in_moscow():
    users = []
    query = "location:Moscow followers:>50"
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/search/users?q={query}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Error fetching data: {response.json()}")
            break

        data = response.json()
        users.extend(data['items'])
        
        if len(data['items']) < per_page:
            break

        page += 1
        time.sleep(1)

    return users

# --- Step 2: Fetch Detailed User Information ---
def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error fetching user {username}: {response.json()}")
        return None

    user_data = response.json()
    return {
        'login': user_data['login'],
        'name': user_data.get('name', ''),
        'company': clean_company_name(user_data.get('company', '')),
        'location': user_data.get('location', ''),
        'email': user_data.get('email', ''),
        'hireable': str(user_data.get('hireable', '')).lower(),
        'bio': user_data.get('bio', ''),
        'public_repos': user_data.get('public_repos', 0),
        'followers': user_data.get('followers', 0),
        'following': user_data.get('following', 0),
        'created_at': user_data.get('created_at', '')
    }

def clean_company_name(company):
    if company:
        company = company.strip().upper()
        if company.startswith('@'):
            company = company[1:]
    return company

# --- Step 3: Fetch User Repositories ---
def get_user_repos(username):
    repos = []
    page = 1
    per_page = 100

    while len(repos) < 500:
        url = f"https://api.github.com/users/{username}/repos?per_page={per_page}&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Error fetching repos for {username}: {response.json()}")
            break

        data = response.json()
        for repo in data:
            repos.append({
                'login': username,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'] or '',
                'has_projects': str(repo.get('has_projects', False)).lower(),
                'has_wiki': str(repo.get('has_wiki', False)).lower(),
                'license_name': repo['license']['key'] if repo.get('license') else ''
            })

        if len(data) < per_page:
            break

        page += 1
        time.sleep(1)

    return repos

# --- Step 4: Save Data to CSV Files ---
def save_users_to_csv(users):
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'login', 'name', 'company', 'location', 'email', 'hireable', 'bio',
            'public_repos', 'followers', 'following', 'created_at'
        ])
        writer.writeheader()
        writer.writerows(users)

def save_repos_to_csv(repos):
    with open('repositories.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'login', 'full_name', 'created_at', 'stargazers_count',
            'watchers_count', 'language', 'has_projects', 'has_wiki', 'license_name'
        ])
        writer.writeheader()
        writer.writerows(repos)

# --- Main Execution ---
if __name__ == "__main__":
    # Fetch and save user data
    users_list = fetch_users_in_moscow()
    user_details = [get_user_details(user['login']) for user in users_list if get_user_details(user['login'])]
    save_users_to_csv(user_details)

    # Fetch and save repositories for each user
    all_repos = []
    for user in user_details:
        all_repos.extend(get_user_repos(user['login']))
    save_repos_to_csv(all_repos)

    print("Data collection complete.")
