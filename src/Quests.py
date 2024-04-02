import requests
from sys import argv
from database import MongoDB
import json
import sys

db = MongoDB()


# accept quest
def accept_quest(user, quest):
    # load quests
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)
    # quest exists?
    if quest in quests:
        user_data = db.download_user_data(user)

        # initialize accepted quests if needed
        if 'accepted' not in user_data['user_data']:
            user_data['user_data']['accepted'] = dict()

        # only can accept one quest at a time
        if not user_data['user_data']['accepted']:
            # initialize tasks for the accepted quest
            tasks = quests[quest]
            user_data['user_data']['accepted'][quest] = dict()
            for task, task_data in tasks.items():
                # Initialize the task with completion status, ignore metadata
                if task != 'metadata':
                    user_data['user_data']['accepted'][quest][task] = {'completed': False}
            # Update user data
            db.update_data(user_data)
            return f'Successfully accepted {quest}'
        else:
            return 'You can only accept one quest at a time! Complete you current quest first!'
    else:
        return 'Invalid quest! please input /accept Q#'



# FOR GitHub actions workflow, WILL exit prematurely if used in code
def check_quest_accepted(user, quest):
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)

    if quest in quests:
        user_data = db.download_user_data(user)
        if user_data['user_data'].get('accepted') is not None:
            if quest in user_data['user_data']['accepted']:
                sys.exit(0)  # success

    sys.exit(1)  # fail


# FOR python scripts as supporting function
def is_quest_accepted(user, quest):
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)

    if quest in quests:
        user_data = db.download_user_data(user)
        if user_data['user_data'].get('accepted') is not None:
            if quest in user_data['user_data']['accepted']:
                return True

    return False


# remove quest
def remove_quest(user):
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)

    user_data = db.download_user_data(user)
    try:
        del user_data['user_data']['accepted']
        db.update_data(user_data)
        return 'Quest successfully dropped!'
    except KeyError:
        return 'Quest drop failed, please ensure there is a quest to drop.'



# complete quest
def complete_quest(user, quest):
    user_data = db.download_user_data(user)

    # check if the quest accepted by the user
    if 'accepted' in user_data['user_data'] and quest in user_data['user_data']['accepted']:
        # big one, basically just checking that ALL tasks under quest are true
        tasks_completed = all(
            user_data['user_data'].get(task, {}).get('completed', False) for task in user_data['user_data'][quest])

        # all tasks related to the quest are completed
        if tasks_completed:
            # remove from accepted quests
            user_data['user_data']['accepted'].remove(quest)

            # add quest ID to completed quests
            if 'completed' not in user_data['user_data']:
                user_data['user_data']['completed'] = []
            user_data['user_data']['completed'].append(quest)

            # update user data
            db.update_data(user_data)
            return True  # quest successfully completed
    return False  # quest not completed


def complete_task(user, quest, task):
    user_data = db.download_user_data(user)
    # load quests
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)

    points = quests[quest][task]['points'] # TODO: potential key issue here
    print(f"User got {points} points")

    # check quest is accepted by the user and the task exists
    if 'accepted' in user_data['user_data'] and quest in user_data['user_data']['accepted'] \
            and task in user_data['user_data']['accepted'][quest]:
        # Mark the task as completed
        user_data['user_data']['accepted'][quest][task]['completed'] = True
        user_data['user_data'][points] += points

        # Update user data
        db.update_data(user_data)
        return True
    return False  # not completed


def display_quests(user):
    response = ''
    # TODO: later implement a check for prerequisite met, prob a simple if statement with iterator
    with open("src/AvailableQuests.json") as file:
        quests = json.load(file)

    user_data = db.download_user_data(user)

    if user_data is None:
        return 'Please comment /new to create user'
    else:
        if 'completed' in user_data['user_data']:
            completed_quests = user_data['user_data']['completed']
        else:
            completed_quests = []

        for quest_id, quest_data in quests.items():
            if quest_id not in completed_quests:
                response += quest_id + ': ' + quest_data["metadata"]["title"] + '\n'
        return 'Available quests: \n' + response + 'Please respond with /accept <Q# --> corresponding quest number>'


if __name__ == '__main__':
    user = argv[1]
    command = argv[2]
    if len(argv) == 4:
        quest = argv[3]
    # generate character
    if command == 'new':
        db.create_user(user)
    if command == 'accept':
        accept_quest(user, quest)
    if command == 'drop':
        remove_quest(user, quest)
    if command == 'display':
        print(display_quests(user))
    if command == 'check':
        check_quest_accepted(user, quest)
