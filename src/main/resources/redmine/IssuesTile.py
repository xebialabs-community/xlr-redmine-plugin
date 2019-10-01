
from redmine import RedmineServer
redmine = RedmineServer(redmineServer)

count = 0
data = {}
result = []

if issues != None:
    count = len(issues)

issuesIds = []
for loop in issues:
    issuesIds.append(loop)

issuesDetails = redmine.getIssuesDetails(issuesIds, None, None)

for d in issuesDetails: 
    result.append({
        'id': d['id'],
        'subject': d['subject'],
        'author': d['author']['name'],
        'description': d['description'],
        'priority': d['priority']['name'],
        'startDate': d['start_date']
    })

data = {
    "count": count,
    "issues": result,
    "url": redmineServer['url']
}
