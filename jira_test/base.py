import datetime
import time
from unittest import TestCase

from docstring_parser import parse

from jira_test.config import SUBMIT_TEST_JIRA
from jira_test.constants import TestExecuteStatus, DATETIME_FORMAT
from jira_test.jira import JiraTestCase, JiraTestResult
from jira_test.jira.listener import Listener


class TestBase(TestCase):
    ISSUE_KEYS = None
    FOLDER = None

    @classmethod
    def setUpClass(cls):
        cls.listener = None
        if cls.ISSUE_KEYS and cls.FOLDER and SUBMIT_TEST_JIRA:
            try:
                cls.listener = Listener(issue_links=cls.ISSUE_KEYS)
                cls.listener.start_suite()
            except:
                cls.listener = None
        super(TestBase, cls).setUpClass()

    def setUp(self):
        super(TestBase, self).setUp()
        self._testInputData = None
        self._testExpectedData = None
        self._actualResult = None
        self._description = ''
        self._startTime = time.time()

    def _feed_error_and_failure(self):
        result = self.defaultTestResult()
        self._feedErrorsToResult(result, self._outcome.errors)
        error = self.list2reason(result.errors)
        failure = self.list2reason(result.failures)
        return error, failure

    def _get_test_case_key(self):
        docstring = parse(self._testMethodDoc)
        name = docstring.short_description.strip()
        pre_condition = docstring.long_description
        input_data = self._testInputData
        expected_data = self._testExpectedData
        description = self._description
        test_case = JiraTestCase(name=name, pre_condition=pre_condition,
                                 input_data=input_data,
                                 expected_data=expected_data,
                                 folder=self.FOLDER, description=description)
        test_case_key = test_case.create_test_case(self.ISSUE_KEYS)
        return test_case_key

    def _get_test_result(self, test_case_key):
        execution_time = time.time() - self._startTime
        error, failure = self._feed_error_and_failure()
        ok = not error and not failure
        if ok:
            status = TestExecuteStatus.PASS.value
            comment = self._actualResult
        else:
            status = TestExecuteStatus.FAIL.value
            typ, text = ('ERROR', error) if error else ('FAIL', failure)
            msg = [x for x in text.split('\n')[1:] if not x.startswith(' ')][0]
            comment = self._actualResult
        test_result = JiraTestResult(test_case_key=test_case_key, status=status,
                                     execution_time=execution_time,
                                     comment=comment)
        return test_result

    def tearDown(self):
        super(TestBase, self).tearDown()
        if self.listener:
            try:
                test_case_key = self._get_test_case_key()
                test_result = self._get_test_result(test_case_key)
                self.listener.end_test(test_result=test_result)
            except Exception as e:
                print(e)
                pass

    @classmethod
    def tearDownClass(cls):
        if cls.listener:
            cls.listener.end_suite(name=(datetime.datetime.now() + datetime.timedelta(hours=7)).strftime(DATETIME_FORMAT) + ' ' + str(cls.__module__))
        super(TestBase, cls).tearDownClass()

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    @staticmethod
    def response_code(data):
        return data['code']

    @staticmethod
    def response_result(data):
        return data['result']

    @staticmethod
    def refresh(*args):
        for entity in args:
            entity.refresh_from_db()

    @staticmethod
    def get_dict_contain_only_certain_keys(dict_instance: dict, keys: list):
        return {
            key: dict_instance.get(key)
            for key in keys
        }
