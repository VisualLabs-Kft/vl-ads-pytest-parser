# Pytest Parser to Azure DevOps Test Case
Associate DevOps test cases with pytest XML results


## Usage
The parser should be run on an Azure DevOps ```pytest-azurepipelines``` generated XML file, because it searches for the following attributes:
- testcase
  - name
  - result

The Python script requires the following arguments:
- org: Azure DevOps organization name
- project: Azure DevOps project name
- plan: Azure DevOps test plan name
- suite: Azure DevOps test suite name
- auth: Azure DevOps personal access token
- xml: pytest-azurepipelines generated XML file

For example:
```
ads-pytest-parser org project planID suiteID authToken test.xml
```

The script will then associate the test cases with the test results - for the test cases the outcome will be set.