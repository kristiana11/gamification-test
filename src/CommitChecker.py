import requests
from sys import argv
from database import MongoDB
import json


def check_commits(user, repo, branch):
    url = f"https://api.github.com/repos/{repo}/commits?sha={branch}"

    response = requests.get(url)
    if response.status_code == 200:
        commits = response.json()
        db = MongoDB()
        # extract authors of commits
        commit_authors = [commit['author']['login'] for commit in commits if commit['author'] is not None]

        # check if the user has committed to the branch
        if user in commit_authors:
            print('User has created their first commit')
            with open('src/AvailableQuests.json', 'r') as file:
                quests = json.load(file)
            user_data = db.download_user_data(user)
            user_data['user_data']['xp'] += quests['first_commit']['xp']
            # TODO: remove from accepted quests, add to completed quests, implement positive feedback
            # (comment quest completed via POST request)
            user_data['user_data']['accepted'].remove('first_commit')
            if user_data['user_data'].get('completed') is not None:
                user_data['user_data']['completed'] += ['first_commit']
            else:
                user_data['user_data']['completed'] = ['first_commit']
            db.update_data(user_data)
        else:
            print('User has not created their first commit')


if __name__ == '__main__':
    repo_owner = argv[1]
    repo_name = argv[2]
    repo_branch = argv[3]

    check_commits(repo_owner, repo_name, repo_branch)
