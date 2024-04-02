import os
from sys import argv
import requests
import json
import Quests
from database import MongoDB

def post_comment(repo, issue_number, comment_body):
    # GitHub's authentication token
    token = os.getenv('GH_TOKEN')

    # API endpoint for creating a comment on an issue
    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/comments'

    # Request headers
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Request body
    data = {
        'body': comment_body
    }

    # Send POST request to create a comment
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 201:
        print('Comment posted successfully.')
    else:
        print(f'Failed to post comment. Status code: {response.status_code}')
        print(response.text)


if __name__ == "__main__":
    # GitHub repository information
    repo = argv[1]
    user = repo.split('/')[0]
    # Issue number where the comment will be posted
    issue_number = argv[2]  # Replace with the actual issue number
    command = argv[3]
    # quest = argv[3].split(' ')[1]
    if len(argv) > 4:
        quest = argv[4] #maybe add list slicing
        print(argv)

    # Comment to be posted

    if command == '/display':
        comment_body = Quests.display_quests(user)
        # Post the comment
    # user calls accept
    elif command == '/new':
        db = MongoDB()
        comment_body = 'Attempting to create new user'  # later should make create user DB function return feedback
        db.create_user(user)

    elif command == '/accept':
        # Call the function to accept the quest and add it to the user's database profile
        comment_body = Quests.accept_quest(user, quest)
    elif command == '/drop':
        comment_body = Quests.remove_quest(user)
    else:
        comment_body = 'Invalid input, available commands: /display /newuser /drop /accept <Q#>'  # TODO: need to work on

    post_comment(repo, issue_number, comment_body)
    print(f"you said: ${argv[3:]}")
