__author__ = 'sdouglas'

import re
import xml.etree.ElementTree as ET


class Parse():
    def __init__(self, filename):
        self.filename = filename

    def load_xml_tree(self):
        return ET.parse(self.filename)

    @staticmethod
    def find_doc_namespace(element):
        try:
            return re.match("^{.*}", element.find(".").tag).group(0)
        except TypeError as te:
            print "Element has no namespace or an object.\n" + str(te)
            return ""

    def construct_dictionary(self):
        try:
            root = self.load_xml_tree()
            dict_list = list()
            for group in root.findall(".//"+self.find_doc_namespace(root)+"Group"):
                dict_list.append(self.parse_group_dictionary(group))
            return dict_list
        except ET.ParseError as xml_error:
            print "Error: not a valid xml file." + str(xml_error)
            exit()
        except Exception as e:
            print "Could not parse file." + str(e)

    def parse_group_dictionary(self, group_element):
        stig_dict = dict()
        # Description info located as children of the Group tag
        stig_dict['STIG_ID'] = group_element.attrib['id']
        rule_element = group_element.find(self.find_doc_namespace(group_element)+"Rule")
        stig_dict['SRG_ID'] = rule_element.attrib['id']
        stig_dict['SRG_SEVERITY'] = rule_element.attrib['severity']
        stig_dict['SRG_WEIGHT'] = rule_element.attrib['weight']
        # Useful info located in the rule section
        stig_dict['VERSION'] = rule_element.find(".//"+self.find_doc_namespace(group_element)+"version").text
        stig_dict['TITLE'] = rule_element.find(".//"+self.find_doc_namespace(group_element)+"title").text
        stig_dict['DESCRIPTION'] = rule_element.find(".//"+self.find_doc_namespace(group_element)+"description").text
        stig_dict['FIX_ID'] = rule_element.find(".//"+self.find_doc_namespace(group_element)+"fix").attrib['id']
        stig_dict['FIX_TEXT'] = rule_element.find(".//"+self.find_doc_namespace(group_element)+"fixtext").text
        return stig_dict

    @staticmethod
    def pretty_print_dict(input_dict):
        print "\n\n"
        print (
            "###############\nSTIG: %s\n###############\n"
            "SRG ID: %s\t"
            "Severity: %s\t"
            "Weight: %s"
        ) % (input_dict['STIG_ID'], input_dict['SRG_ID'], input_dict['SRG_SEVERITY'], input_dict['SRG_WEIGHT'])
        print "---------------------------"
        print (
            "[+] Version: %s\n"
            "[+] Title: %s\n"
            "[+] Description: %s\n"
            "[+] Fix: %s\n"
            "%s"
        ) % (input_dict['VERSION'], input_dict['TITLE'], input_dict['DESCRIPTION'], input_dict['FIX_ID'],
             input_dict['FIX_TEXT'])
        print "---------------------------"
