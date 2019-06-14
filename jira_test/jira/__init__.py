import requests
from datetime import datetime

from jira_test.config import PROJECT_KEY
from jira_test.constants import TestCaseStatus, TestCasePriority, \
    JIRA_DATETIME_FORMAT
from jira_test.helpers import json_dump
from jira_test.jira.jira_api import jira_service_api


class IssueLink:
    def __init__(self, jira_settings):
        ''' Create a test cycle with a set of test cases and execution result of each test case.
            The test execution results could have come from an automated test tool.
        :param jira_settings:
        :param key: key of issue-link
        '''
        self._jira_settings = jira_settings
        self._auth_string = (
        self._jira_settings['user'], self._jira_settings['password'])
        self.url = self._jira_settings['url'] + '/rest/api/latest/issue/'

    def get_issue_link_status(self, key):
        print(requests.get(self.url + key, auth=self._auth_string))
        return \
        requests.get(self.url + key, auth=self._auth_string).json()['fields'][
            'status']['name']


class JiraTestCase(object):
    '''
    Jira Test Case object to save a instance of a test case Jira
    '''

    def __init__(self, name, pre_condition=None, objective=None, folder=None,
                 status=TestCaseStatus.APPROVED.value,
                 input_data=None, expected_data=None,
                 priority=TestCasePriority.HIGH.value, description=None):
        assert name
        self.name = name
        self.pre_condition = pre_condition
        self.objective = objective
        self.folder = folder
        self.status = status
        self.input_data = input_data
        self.expected_data = expected_data
        self.priority = priority
        self.description = description

    def create_test_case(self, issue_links):
        pre_condition = self.pre_condition or ''
        pre_condition = pre_condition.replace('\n', '<br>')
        test_case_data = {
            'name': self.name,
            'projectKey': PROJECT_KEY
            ,
            'issueLinks': issue_links,
            'status': self.status,
            'priority': self.priority,
            'precondition': pre_condition,
            'folder': self.folder,
            'testScript': {
                'type': 'STEP_BY_STEP',
                'steps': [
                    {
                        'description': self.description,
                        'testData': '<pre>' + json_dump(self.input_data,
                                                        indent=4) + '</pre>',
                        'expectedResult': '<pre>' + json_dump(
                            self.expected_data, indent=4) + '</pre>'
                    }
                ]
            }
        }
        return jira_service_api.create_test_case(test_case_data=test_case_data)


class JiraTestResult(object):
    '''
    Save test result after execute a test case
    '''

    def __init__(self, test_case_key, status, execution_time=None,
                 execution_date=None, comment=None):
        if not execution_date:
            execution_date = datetime.now()
        self.test_case_key = test_case_key
        self.status = status
        self.execution_time = execution_time
        self.execution_date = execution_date
        self.comment = comment

    def toJSON(self):
        return {
            'testCaseKey': self.test_case_key,
            'status': self.status,
            'executionTime': self.execution_time,
            'executionDate': self.execution_date.strftime(JIRA_DATETIME_FORMAT),
            'scriptResults': [
                {
                    'index': 0,
                    'status': self.status,
                    'comment': '<pre>' + json_dump(self.comment,
                                                   indent=4) + '</pre>'
                }
            ]
        }


class JiraTestRun(object):
    def __init__(self, name, issue_key, test_results, start_date=None,
                 end_date=None):
        now = datetime.now()
        start_date = start_date or now
        end_date = end_date or now
        self.name = name
        self.issue_key = issue_key
        self.start_date = start_date
        self.end_date = end_date
        self.test_results = test_results

    def create_test_run(self):
        test_run_data = {
            'name': self.name,
            'projectKey': PROJECT_KEY,
            'issueKey': self.issue_key,
            'plannedStartDate': self.start_date.strftime(JIRA_DATETIME_FORMAT),
            'plannedEndDate': self.end_date.strftime(JIRA_DATETIME_FORMAT),
            'items': self.test_results
        }
        jira_service_api.create_test_run(test_run_data=test_run_data)
