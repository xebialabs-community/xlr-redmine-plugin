#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from redmine import RedmineServer

if redmineServer != None:
    redmine = RedmineServer(redmineServer)
    
    count = 0
    data = {}
    result = []
    if issues != None and len(issues)>0:
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
    else:
        data = {
            "count": 0
        }
else:

    data = {
        "count": 0
    }