import requests


def check_pull_requests(repo_owner, repo_name):
    print("checking pull requests:")
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    response = requests.get(url)
    if response.status_code == 200:
        pull_requests = response.json()
        for pr in pull_requests:
            print(f"Pull Request #{pr['number']}: {pr['title']}")
    else:
        print("Failed to fetch pull requests")


if __name__ == '__main__':
    repository_owner = "caiton1"
    repository_name = "gamification-demo"
    check_pull_requests(repository_owner, repository_name)
