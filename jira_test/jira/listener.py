from jira_test.jira import IssueLink, JiraTestResult, JiraTestRun
from jira_test.jira.jira_api import jira_service_api, JIRA_SETTINGS


class Listener(object):

    def __init__(self, issue_links=None):
        if issue_links is None:
            issue_links = []
        self.execution_result = []
        self.issue_links = issue_links
        self.testCaseKeys = {}

    def start_suite(self):
        """
            :param name: test suite's name
            :param attrs: attribute dictionary of test suite
            """
        self.issue_links = [issue for issue in self.issue_links if
                            IssueLink(JIRA_SETTINGS).get_issue_link_status(
                                issue) != 'Closed']
        if len(self.issue_links) > 0:
            # Get list test case associated to a list of issue and delete it =>> Test cases will be deleted in this
            # issue and Test Management tool but not delete test cases in previous cycles
            tc_list = jira_service_api.get_list_test_case_in_issue(
                self.issue_links)
            for test in tc_list:
                jira_service_api.delete_test_case(test)
        else:
            raise Exception("issueLinks is None")

    def end_test(self, test_result: JiraTestResult):
        """ Append test result to test run """
        self.execution_result.append(test_result.toJSON())

    def end_suite(self, name):
        """
            Called when a test suite ends.
            :param name:
            :param attrs:
            """
        if self.execution_result:
            for issue_key in self.issue_links:
                test_run = JiraTestRun(name=name, issue_key=issue_key,
                                       test_results=self.execution_result)
                test_run.create_test_run()
