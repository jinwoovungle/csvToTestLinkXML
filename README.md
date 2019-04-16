How to create test cases in csv format

- use the csv template file ./templates/testlink_testcase_template_vungle.csv
- refer to the google doc for detail at 
https://docs.google.com/document/d/1nhJNLarN6dwZz6cT3CLVLBnjlHp3Xld_N81_g415CRg/edit?usp=sharing

How to use csv2tlxml.py to convert csv file to TestLink XML
  
    $ python csv2tlxml.py -h
      usage: csv2tlxml.py [-h] [-c CSV_FILE] [-s PARENT_TS_NAME] [-v VALIDATE_XML]

      optional arguments:
        -h, --help            show this help message and exit
        -c CSV_FILE, --csvfile CSV_FILE
                                test suite file in csv format
        -s PARENT_TS_NAME, --testsuite PARENT_TS_NAME
                                the parent test suite name
        -v VALIDATE_XML, --validate-xml VALIDATE_XML
                                validate the xml format
  
- If the TestLink XML file is generated with the parent test suite name provided with "-s", the parent test suite will be created under the selected test suite and the test suites of test cases from csv file will be imported under the newly created parent test suite in TestLink

      $ python csv2tlxml.py -c [CSV_FILE_PATH] -s [NEW_PARENT_TESTSUITE_NAME]

- If the TestLink XML file is generated without the parent test suite name, the test suites of test cases from csv file will be imported under the selected parent test suite in TestLink

      $ python csv2tlxml.py -c [CSV_FILE_PATH]

- To validate the existing TestLink XML format

      $ python csv2tlxml.py -v [XML_FILE_PATH]

refer to the google doc for detail at 
https://docs.google.com/document/d/1nhJNLarN6dwZz6cT3CLVLBnjlHp3Xld_N81_g415CRg/edit?usp=sharing
