// main code for managing PRs. main functions are create and delete
const github = require('@actions/github');


try {
    const action = process.env.INPUT_ACTION;
    const user = process.env.INPUT_USER;
    const description = process.env.INPUT_DESCRIPTION;

    const octokit = github.getOctokit(process.env.GH_TOKEN);

    switch (action) {
        case 'create':
            // create PR
            const response = octokit.rest.pulls.create({
                owner: github.context.repo.owner,
                repo: github.context.repo.repo,
                title: description,
                head: user,
                base: 'main',
                body: description
            });

            octokit.request('POST /repos/${github.context.repo.owner}/${github.context.repo.repo}/pulls', {
                owner: github.context.repo.owner,
                repo: github.context.repo.repo,
                title: description,
                body: description,
                head: user,
                base: {'X-GitHub-Api-Version': '2022-11-28'}

            })
            console.log('Pull request created:', response.data.html_url);
        break;
        case 'delete':
            // delete PR
            const pulls = octokit.rest.pulls.list({
                owner: github.context.repo.owner,
                repo: github.context.repo.repo,
                state: 'open',
                head: `${user}:main`
            });
            if (pulls.data.length > 0) {
                octokit.rest.pulls.update({
                    owner: github.context.repo.owner,
                    repo: github.context.repo.repo,
                    pull_number: pulls.data[0].number,
                    state: 'closed'
                });
                console.log('Pull request deleted');
            }
            else {
                console.log('No open pull request found for the specified user');
            }
        break;
      default:
        console.log('Invalid action specified');
    }
}
catch (error) {
    console.log(error.message);
}


