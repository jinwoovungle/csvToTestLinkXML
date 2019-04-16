import argparse
import csv
import os
from xml.etree import ElementTree
from xml.etree.ElementTree import ParseError

class xmlBuilder(object):
    def __init__(self):
        self.__xml_str = []

    def append(self, str_line):
        self.__xml_str.append(str_line)
        return self

    def getByLine(self, line_no):
        return self.__xml_str[line_no-1]

    def toXMLStr(self, joinBy="\n"):
        return joinBy.join(self.__xml_str)

    def save(self, path):
        try:
            with open(path, "w") as xml_file:
                xml_file.write(self.toXMLStr())
            print("\nsaved to %s" % path)
            xmlValidator(path).run()
        except:
            print("\nfailed to save to %s" % path)


class csv2TestLinkXml(object):

    __DEFAULT_EXECUTION_TYPE = "1"
    __DEFAULT_STATUS = "1"
    __DEFAULT_IMPORTANCE = "3"
    __DEFAULT_IS_OPEN = "1"
    __DEFAULT_ACTIVE = "1"

    def __init__(self, csv_file, ts_name):
        self.__csv_file = os.path.abspath(csv_file)
        self.__dir_name = os.path.dirname(self.__csv_file)
        self.__csv_filename = os.path.basename(self.__csv_file)
        self.__xml_filename = '.'.join(['.'.join(self.__csv_file.split('.')[0:-1]), 'xml'])
        self.__ts_name = ts_name if ts_name != None else ''
        self.__testlink_xml = xmlBuilder()

    def parseCsv2DictList(self):
        print("\ncsv file reading started ....... \n%s" % self.__csv_file)
        try:
            with open(self.__csv_file, 'r', encoding='utf-8') as csv_file:
                tl_csv_dictlist = csv.DictReader(csv_file)
                tc_info_by_ts_name = {}
                for tc_row in tl_csv_dictlist:
                    if tc_row['test_suite'] in tc_info_by_ts_name.keys():
                        tc_info_by_ts_name[tc_row['test_suite']].append(tc_row)
                    else:
                        tc_info_by_ts_name[tc_row['test_suite']] = [tc_row]
                self.__tc_info = tc_info_by_ts_name

            print("\ncsv file reading completed ....... ")
        except:
            print("\ncsv file reading failed ....... \nexit the script")
            exit()

        return self

    def convert2Xml(self):
        print ("\nconverting to testlink XML started .......")

        self.addHeader()
        for ts_name in self.__tc_info.keys():
            self.addTestSuite(ts_name)
            for tc_info in self.__tc_info[ts_name]:
                self.addTestCase(tc_info)
                self.addTestStep(tc_info)
                self.closeTestCase()
            self.closeTestSuite()
        self.closeTestSuite()
        print("converting to testlink XML completed .......")

        self.__testlink_xml.save(self.__xml_filename)

        return self

    def addHeader(self):
        self.__testlink_xml\
            .append('<?xml version="1.0" encoding="UTF-8"?>') \
            .append('<testsuite id="" name="%s" >' % self.__ts_name) \
            .append('<node_order><![CDATA[]]></node_order>') \
            .append('<details><![CDATA[]]></details>')
        return self

    def addTestSuite(self, ts_name):
        self.__testlink_xml \
            .append('<testsuite id="" name="%s" >' % self.__converToHTML(ts_name, splitBy="\n", joinBy=" ")) \
            .append('\t<node_order><![CDATA[1]]></node_order>') \
            .append('\t<details><![CDATA[]]></details>')
        return self

    def closeTestSuite(self):
        self.__testlink_xml.append("</testsuite>")
        return self

    def addTestCase(self, tc_info):

        test_name = self.__converToHTML(tc_info['name'], splitBy="\n", joinBy=" ")
        summary = self.__converToHTML(tc_info['summary'], splitBy="\n", joinBy="<br>")
        preconditions = self.__converToHTML(tc_info['preconditions'], splitBy="\n", joinBy="<br>")
        execution_type = self.__DEFAULT_EXECUTION_TYPE if "execution_type" not in tc_info.keys() else tc_info['execution_type']
        status = self.__DEFAULT_STATUS if "status" not in tc_info.keys() else tc_info['status']

        self.__testlink_xml \
            .append('<testcase internalid="" name="%s">' % test_name) \
            .append('\t<node_order><![CDATA[1000]]></node_order>') \
            .append('\t<externalid><![CDATA[]]></externalid>') \
            .append('\t<version><![CDATA[1]]></version>') \
            .append('\t<summary><![CDATA[<p>%s</p>]]></summary>' % summary) \
            .append('\t<preconditions><![CDATA[<p>%s</p>]]></preconditions>' % preconditions) \
            .append('\t<execution_type><![CDATA[%s]]></execution_type>' % execution_type) \
            .append('\t<estimated_exec_duration></estimated_exec_duration>') \
            .append('\t<status>%s</status>' % status) \
            .append('\t<is_open>%s</is_open>' % self.__DEFAULT_IS_OPEN) \
            .append('\t<active>%s</active>' % self.__DEFAULT_ACTIVE)
        return self

    def closeTestCase(self):
        self.__testlink_xml.append("</testcase>")
        return self

    def addTestStep(self, tc_info):
        execution_type = self.__DEFAULT_EXECUTION_TYPE \
            if "execution_type" not in tc_info.keys() else tc_info['execution_type']
        steps = self.__converToHTML(tc_info['steps'], splitBy="\n", joinBy="<br>")
        expected_results = self.__converToHTML(tc_info['expected_results'], splitBy="\n", joinBy="<br>")

        self.__testlink_xml \
            .append('<steps>')\
            .append('<step>') \
            .append('\t<step_number><![CDATA[1]]></step_number>') \
            .append('\t<actions><![CDATA[<p>%s</p>]]></actions>' % steps) \
            .append('\t<expectedresults><![CDATA[<p>%s</p>]]></expectedresults>' % expected_results) \
            .append('\t<execution_type><![CDATA[%s]]></execution_type>' % execution_type) \
            .append('</step>') \
            .append('</steps>')
        return self

    def __validateXMLAttr(self, attr_str):
        attr_replacement_list = [["\"", "&quot;"],
                                ["<", ""],
                                [">", ""]]

        for find, replace in attr_replacement_list:
            if "\"" in attr_str:
                attr_str = attr_str.replace(find, replace)
        return attr_str

    def __converToHTML(self, str_info, splitBy="\n", joinBy="<br>"):
        return joinBy.join([self.__validateXMLAttr(x.strip()) for x in str_info.split(splitBy)])


class xmlValidator(object):
    def __init__(self, xml_filename):
        self.__xml_filename = xml_filename

    def read(self):
        self.__xml_lines = open(self.__xml_filename, "r").readlines()
        return self

    def readLine(self, line_no):
        return self.__xml_lines[line_no-1]

    def printXMLFormatError(self, err_msg):
        print(self.__xml_filename)
        print("error message: " + err_msg)
        line_no = int(err_msg.split(":")[1].split(',')[0].strip().split(' ')[1])
        print ("Line %d: %s" % (line_no, self.read().readLine(line_no)))

    def run(self):
        print("\n[XML Format Validation]\n%s" % self.__xml_filename)
        try:
            ElementTree.parse(self.__xml_filename)
            print ("XML Format validation passed.....")
        except ParseError as pe:
            print ("XML Format validation failed.....")
            self.printXMLFormatError(str(pe))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csvfile', action='store', dest='csv_file', help='test suite file in csv format', required=False)
    parser.add_argument('-s', '--testsuite', action='store', dest='parent_ts_name',help='the parent test suite name', required=False)
    parser.add_argument('-v', '--validate-xml', action='store', dest='validate_xml', help='validate the xml format', required=False)
    results = parser.parse_args()

    if results.validate_xml is not None and os.path.exists(results.validate_xml):
        xmlValidator(results.validate_xml).run()
        exit()

    csv2TestLinkXml(results.csv_file, results.parent_ts_name) \
        .parseCsv2DictList() \
        .convert2Xml()