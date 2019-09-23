#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import com.xhaus.jyson.JysonCodec as json

if redmineServer is None:
    print "No server provided."
    sys.exit(1)
  

ISSUE_CREATED_STATUS = 201

redmineUrl = redmineServer['url']
redmineAPIKey = redmineServer['apiKey']

content="""
{
  "issue": {
    "project_id": %s,
    "subject": "%s",
    "priority_id": %s
  }
}""" % (projectId, subject, priorityId)

headers = {'X-Redmine-API-Key': redmineAPIKey }

request = HttpRequest(redmineServer)
response = request.post('/issues.json', content, contentType = 'application/json', headers = headers)

if response.status == ISSUE_CREATED_STATUS:

    print response.status
    print response.response
    print response.headers

    if response.headers['Content-Type'].startswith('application/json'):
        data = json.loads(response.response)
        issueId = data.get('issues.id')
        print "Created issue %s in Redmine at %s." % (issueId, redmineUrl)
else:
    print "Failed to create issue in Redmine at %s." % redmineUrl
    response.errorDump()
    sys.exit(1)