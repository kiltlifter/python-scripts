__author__ = 'sdouglas'


import xml.etree.ElementTree as ET
import re
from XCCDF_Parser import Parse as xccdf_parser


SAMPLE_STIG = "/home/sdouglas/information-assurance/redhat-stig/U_RedHat_6_V1R7_STIG_SCAP_1-1_Benchmark-xccdf.xml"


def load_xml_tree(file):
    return ET.parse(file)


def find_doc_namespace(element):
    try:
        return re.match("^{.*}", element.find(".").tag).group(0)
    except TypeError as te:
        print "Element has no namespace or an object.\n" + str(te)
        return ""


def get_group_info(group_element):
    stig_dict = dict()
    # Description info located as children of the Group tag
    stig_dict['STIG_ID'] = group_element.attrib['id']
    rule_element = group_element.find(find_doc_namespace(group_element)+"Rule")
    stig_dict['SRG_ID'] = rule_element.attrib['id']
    stig_dict['SRG_SEVERITY'] = rule_element.attrib['severity']
    stig_dict['SRG_WEIGHT'] = rule_element.attrib['weight']
    # Useful info located in the rule section
    stig_dict['VERSION'] = rule_element.find(".//"+find_doc_namespace(group_element)+"version").text
    stig_dict['TITLE'] = rule_element.find(".//"+find_doc_namespace(group_element)+"title").text
    stig_dict['DESCRIPTION'] = rule_element.find(".//"+find_doc_namespace(group_element)+"description").text
    stig_dict['FIX_ID'] = rule_element.find(".//"+find_doc_namespace(group_element)+"fix").attrib['id']
    stig_dict['FIX_TEXT'] = rule_element.find(".//"+find_doc_namespace(group_element)+"fixtext").text
    return stig_dict


def pretty_print_dict(input_dict):
    print "\n\n"
    for value in input_dict.itervalues():
        print value


def main():
    xccdf = xccdf_parser(SAMPLE_STIG)
    stig_list = xccdf.construct_dictionary()
    for i in stig_list:
        xccdf.pretty_print_dict(i)
    #root = load_xml_tree(SAMPLE_STIG)
    #name_space = find_doc_namespace(root)
    #xccdf = xccdf_parser(SAMPLE_STIG)
    #root = xccdf.load_xml_tree()
    #name_space = xccdf.find_doc_namespace(root)

    #groups = root.findall(".//"+name_space+"Group")
    #for group in groups:
        #pretty_print_dict(get_group_info(group))
        #stig_dict = xccdf.construct_dictionary(group)
        #xccdf.pretty_print_dict(stig_dict)


if __name__ == "__main__":
    main()
