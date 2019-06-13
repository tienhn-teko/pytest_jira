# coding=utf-8
import os

PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

JIRA_SETTINGS = {
    'url': os.getenv("JIRA_URL"),
    'user': os.getenv("JIRA_USER"),
    'password': os.getenv("JIRA_PASSWORD")
}

SUBMIT_TEST_JIRA = (os.getenv("SUBMIT_TEST_JIRA", "False") == "True")
