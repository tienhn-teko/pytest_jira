import urllib.parse
from operator import itemgetter

import requests

from jira_test.config import SUBMIT_TEST_JIRA, JIRA_SETTINGS, PROJECT_KEY


class JiraServiceAPI(object):
    TEST_CASE_URL = '/rest/atm/1.0/testcase/'
    TEST_CASE_SEARCH_URL = '/rest/atm/1.0/testcase/search/'
    TEST_RUN_URL = '/rest/atm/1.0/testrun/'
    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'

    def __init__(self, jira_url, user_name, password, project_key):
        assert user_name and password and project_key
        self._auth_string = (user_name, password)
        self._project_key = project_key
        self.url = jira_url

    def _call_api(self, path, method=POST, data=None, params=None):
        path = urllib.parse.urljoin(self.url, path)
        if method == self.POST:
            return requests.post(path, json=data, auth=self._auth_string)
        if method == self.GET:
            return requests.get(path, params=params, auth=self._auth_string)
        if method == self.DELETE:
            return requests.delete(path, auth=self._auth_string)
        return None

    def create_test_case(self, test_case_data):
        """ Create a test case at Jira """
        response = self._call_api(path=self.TEST_CASE_URL, data=test_case_data)
        if response.status_code != 201:
            print("Status code: " + str(response.status_code))
            raise Exception("Error creating test cycle.")
        else:
            testCaseKey = response.json()["key"]
            print("Test case created: " + testCaseKey)
            return testCaseKey

    def create_test_run(self, test_run_data):
        """ Create a test run at Jira """
        response = self._call_api(path=self.TEST_RUN_URL, data=test_run_data)
        if response.status_code != 201:
            print("Status code: " + str(response.status_code))
            raise Exception("Error creating test cycle.")
        else:
            print("Test cycle created: " + response.json()["key"])

    def get_list_test_case_in_issue(self, issue_key):
        """ Get list test case linked to the issues
        :param issue_key: list of issue key - get from Jira
        :return: A list of test case key linked to issues
        """
        params = {
            "query": "projectKey = \"%s\" AND issueKeys IN (%s)" % (
                self._project_key, ','.join(['"%s"' % k for k in issue_key]))
        }
        response = self._call_api(path=self.TEST_CASE_SEARCH_URL, params=params,
                                  method=self.GET).json()
        return list(map(itemgetter('key'), response))

    def delete_test_case(self, test_case_key):
        r""" Send a delete request to delete a test case
        :param test_case_key: key of test case will be deleted (get from jira Test Management Tool)
        """
        response = self._call_api(path=self.TEST_CASE_URL + test_case_key,
                                  method=self.DELETE)
        if response.status_code != 204:
            print(response.status_code)
            raise Exception("Error deleting test case")


jira_service_api = None
if SUBMIT_TEST_JIRA:
    jira_service_api = JiraServiceAPI(jira_url=JIRA_SETTINGS['url'],
                                      project_key=PROJECT_KEY,
                                      user_name=JIRA_SETTINGS['user'],
                                      password=JIRA_SETTINGS['password'])
