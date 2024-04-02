const fs = require('fs');
const readmePath = `${process.env.GITHUB_WORKSPACE}/README.md`;
let readmeContent = fs.readFileSync(readmePath, 'utf8');

// get argument inputs, pass into script
const action = process.env.INPUT_ACTION;
const user = process.env.INPUT_USER;
const content = process.env.INPUT_CONTENT || '';
const replacePattern = process.env.INPUT_REPLACE_PATTERN || '';

console.log(content)

// action based off requested action
switch (action) {
  case 'create':
    readmeContent = user
    readmeContent += '\n'
    readmeContent += content; // overwrite/create
    break;
  case 'append':
    readmeContent += '\n' + content; // add to end
    break;
  case 'update':
    // look for specific to replace 
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp
    readmeContent = readmeContent.replace(new RegExp(replacePattern, 'g'), content);
    break;
  case 'delete':
    // delete specific
    readmeContent = readmeContent.replace(new RegExp(content, 'g'), '');
    break;
  default:
    console.log('Invalid action!');
}

// write to file
fs.writeFileSync(readmePath, readmeContent);

console.log('README managed successfully.');