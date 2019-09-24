#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import com.xhaus.jyson.JysonCodec as Json
from util import error
from xlrelease.HttpRequest import HttpRequest
from org.apache.http.client import ClientProtocolException

class RedmineServer:

    def __init__(self, redmine_server):
        if redmine_server is None:
            error(u'No Server provided')
        self.redmine_server = redmine_server

    def getIssues(self, issueIds=None, projectId=None):
        request = self._createRequest()
        issues = {}
        filters = ''
        url = '/issues.json'

        if issueIds != None:
            filters = 'issue_id=' + issueIds
        
        if projectId != None:
            if len(filters) > 0:
                filters += '&'
            filters += 'project_id=' + projectId

        if len(filters) > 0:
            url += '?' + filters

        try:
            response = request.get(url, content=None, contentType='application/json', headers=self._createHeaders())
            if response.status == 200:
                data = Json.loads(response.response)
                for item in data['issues']:
                    id = item['id']
                    subject = item['subject']
                    issues[id] = subject
                return issues
            else:
                error(u'Failed to get issues', response)
        except ClientProtocolException:
            raise Exception()
        
        return issues


    def _createRequest(self):
        params = self.redmine_server.copy()
        if params['apiKey']:
            params.pop('username')
            params.pop('password')
        return HttpRequest(params)

    def _createHeaders(self):
        headers = None
        if self.redmine_server['apiKey']:
            headers = {'X-Redmine-API-Key': self.redmine_server['apiKey'] }
        return headers