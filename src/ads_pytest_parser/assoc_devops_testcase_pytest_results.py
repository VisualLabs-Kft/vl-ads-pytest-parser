# Associate DevOps test cases with pytest XML results
# The code will parse the JUnit XML file and send the results to DevOps Test Plan
# The test cases should be named like this: testcase_1234, where 1234 is the test case ID in DevOps
# The module should be called with the following arguments: org, project, plan, suite, auth (token)

import xml.etree.ElementTree as ET
import requests
import json
import argparse

# TODO: add error logging into the json body
# TODO: how to run this code in the pipeline and how to get the test.xml file in the pipeline?
# TODO: add error handling
# TODO: mark the test case with ID?
# TODO: add logging for pypi
# TODO: rename the package to ads-pytest-parser


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        description="Parse the JUnit XML file and send the results to DevOps Test Plan",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("org", help="DevOps organization")
    parser.add_argument("project", help="DevOps project")
    parser.add_argument("plan", help="DevOps Test Plan ID")
    parser.add_argument("suite", help="DevOps Test Suite ID")
    parser.add_argument("auth", help="DevOps Authetication Token")
    parser.add_argument("xml", help="Path to XML file")

    args = vars(parser.parse_args())

    # Commmand line arguments, DevOps variables and secrets
    ORGANIZATION = args["org"]
    PROJECT = args["project"]
    PLAN_ID = args["plan"]
    SUITE_ID = args["suite"]
    AUTH_TOKEN = args["auth"]
    XML_FILE = args["xml"]

    # Parse the JUnit XML file
    tree = ET.parse(XML_FILE)
    root = tree.getroot()

    # Construct the URL and the header
    URL = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/testplan/Plans/{PLAN_ID}/Suites/{SUITE_ID}/TestPoint?api-version=7.0"
    headers = {
        "Content-Type": "application/json",
    }

    body = []

    # Loop through each test case in the XML file
    for testcase in root.iter("test-case"):

        # Get the test case ID and test result
        # Tests should be named like this: testcase_1234, where 1234 is the test case ID in DevOps
        case_id = testcase.get("methodname").split("_")[1]
        result = testcase.get("result")

        # Print the results
        # print(f"Test case ID: {case_id}, Result: {result}")

        # Build json object
        test_case_json = {
            "id": case_id,
            "results": {
                "outcome": "passed" if result == "Passed" else "failed",
            },
        }

        # create a json array
        body.append(test_case_json)

    print(body)

    # send an http request to the URL
    response = requests.patch(
        URL, headers=headers, auth=("", AUTH_TOKEN), data=json.dumps(body)
    )
    print(response)
