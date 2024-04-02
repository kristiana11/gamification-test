"""
WARNING: DESTRUCTIVE
deletes all workflow runs, due to the heavy reliance on runners in this project, this is nice to have
"""
import requests
import os
import concurrent.futures


# clean up run
def delete_workflow_run(run):
    run_id = run["id"]
    delete_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"
    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted workflow run with ID {run_id}")
    else:
        print(f"Failed to delete workflow run with ID {run_id}. Status code: {response.status_code}")


token = os.environ["GH_TOKEN"]
# TODO: make it more dynamic
owner = "caiton1"
repo = "gamification-demo"

# list of all workflow runs
url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
headers = {"Authorization": f"token {token}"}
all_runs = []
while url:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    all_runs.extend(data["workflow_runs"])
    url = None
    for link in response.headers.get("Link", "").split(","):
        link_info = link.split(";")
        if len(link_info) == 2 and link_info[1].strip() == 'rel="next"':
            url = link_info[0].strip()[1:-1]
            break

# Delete workflow runs concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Map the delete_workflow_run function to each workflow run
    futures = [executor.submit(delete_workflow_run, run) for run in all_runs]

    # Wait for all futures to complete
    for future in concurrent.futures.as_completed(futures):
        pass  # Do nothing, but wait for all tasks to complete
