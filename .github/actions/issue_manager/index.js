const github = require('@actions/github');

try {
    const action = process.env.INPUT_ACTION;
    const user = process.env.INPUT_USER;
    cont title = process.env.INPUT_TITLE;
    const description = process.env.INPUT_DESCRIPTION;

    // Look at how to use octokit to make API calls that will create an issue
    const octokit = github.getOctokit(process.env.GH_TOKEN);
    const { owner, repo } = github.context.repo;

    switch (action) {
        case 'create':
            // create issue
            octokit.rest.issues.create({
                owner: owner,
                repo: repo,
                title: title, // Assuming description as issue title TODO: change
                body: description // Include user in the issue body
            }).then(response => {
                console.log(`Issue created successfully: ${response.data.html_url}`);
            }).catch(error => {
                console.error(`Error creating issue: ${error.message}`);
            });
            break;
        case 'delete':
            // delete issue
            // assuming description contains the issue number
            const issueNumber = parseInt(description);
            if (!isNaN(issueNumber)) {
                octokit.rest.issues.delete({
                    owner: owner,
                    repo: repo,
                    issue_number: issueNumber
                }).then(() => {
                    console.log(`Issue ${issueNumber} deleted successfully`);
                }).catch(error => {
                    console.error(`Error deleting issue ${issueNumber}: ${error.message}`);
                });
            } else {
                console.error(`Invalid issue number: ${description}`);
            }
            break;
        default:
            console.log('Invalid action specified');
    }
} catch (error) {
    console.log(error.message);
}