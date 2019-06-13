# coding=utf-8

import enum


class TestCaseStatus(enum.Enum):
    APPROVED = 'Approved'


class TestCasePriority(enum.Enum):
    LOW = 'Low'
    HIGH = 'High'
    NORMAL = 'Normal'


class TestExecuteStatus(enum.Enum):
    FAIL = 'Fail'
    PASS = 'Pass'


DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
JIRA_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
