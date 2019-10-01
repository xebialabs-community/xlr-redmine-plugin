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
import urllib
from util import error
from xlrelease.HttpRequest import HttpRequest
from org.apache.http.client import ClientProtocolException

class RedmineServer:

    def __init__(self, redmine_server):
        self.content_type = 'application/json'
        self.encoding = 'utf-8'
        if redmine_server is None:
            error(u'No Server provided')
        self.redmine_server = redmine_server

    def getIssuesDetails(self, issueIds=None, projectId=None, otherFields=None):
        request = self._createRequest()
        issues = {}
        filters = ''
        url = '/issues.json'

        if issueIds != None:
            filters = 'issue_id=' + ','.join(issueIds)
        
        if projectId != None:
            if len(filters) > 0:
                filters += '&'
            filters += 'project_id=' + projectId

        if otherFields != None:
            if len(filters) > 0:
                filters += '&'
            for loop in otherFields:
                filters += urllib.quote_plus(loop) + '=' + urllib.quote_plus(otherFields[loop]) + '&'
            filters = filters[:-1]

        if len(filters) > 0:
            url += '?' + filters

        try:
            response = request.get(url, content=None, contentType=self.content_type, headers=self._createHeaders())
            if response.status == 200:
                data = Json.loads(response.response)
                return data['issues']
            else:
                error(u'Failed to get issues', response)
        except ClientProtocolException:
            raise Exception()


    def getIssues(self, issueIds=None, projectId=None, otherFields=None):
        request = self._createRequest()
        issues = {}
        filters = ''
        url = '/issues.json'

        if issueIds != None:
            filters = 'issue_id=' + ','.join(issueIds)
        
        if projectId != None:
            if len(filters) > 0:
                filters += '&'
            filters += 'project_id=' + projectId

        if otherFields != None:
            if len(filters) > 0:
                filters += '&'
            for loop in otherFields:
                filters += urllib.quote_plus(loop) + '=' + urllib.quote_plus(otherFields[loop]) + '&'
            filters = filters[:-1]

        if len(filters) > 0:
            url += '?' + filters

        try:
            response = request.get(url, content=None, contentType=self.content_type, headers=self._createHeaders())
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

    def updateIssue(self, issueId, newStatus, comment):
        request = self._createRequest()
        newContent = {
            'issue': {
                'status_id': int(newStatus),
                'notes': comment
            }
        }
        newContent = self._serialize(newContent)
        url = '/issues/%s.json' % issueId

        try:
            response = request.put(url, newContent, contentType=self.content_type, headers=self._createHeaders())
            if response.status == 200:
                print u'Issue {0} updated'.format(issueId)
            else:
                print u'Error updating issue {0}: {1}'.format(issueId, response)
        except ClientProtocolException:
            raise Exception()



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

    def _serialize(self, content):
        return Json.dumps(content).encode(self.encoding)