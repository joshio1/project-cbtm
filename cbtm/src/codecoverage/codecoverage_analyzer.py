import os
from lxml import etree
from src.lang.c_parser import CParser
from src import settings
import fnmatch
from src import utils
import src.utils
import sys
from src.method_testcase_data_access import MethodTestcaseDataAccess

class CodeCoverageParser:

    def __init__(self,workspace_folder):
        self.language_parser = CParser()
        self.workspace_folder = workspace_folder

    def get_hit_methods_by_code_coverage(self, cobertura_output_xml):
        tree = etree.parse(cobertura_output_xml)
        lines_nodes = tree.xpath(".//lines")
        hit_function_set = set()
        for lines in lines_nodes:
            class_node = (lines.getparent())
            file_path = class_node.attrib["filename"]
            line_rate = float(class_node.attrib["line-rate"])
            if(line_rate > 0): #If line rate is 0, it means that the test has not hit any lines in this file/class.
                full_file_path = "C:\\"+os.path.sep+file_path; #Path from XML does not have "C:"
                relative_path_to_store_in_method = os.path.relpath(full_file_path,self.workspace_folder)
                line_function_mapping = self.language_parser.get_line_function_mapping(full_file_path, relative_path_to_store_in_method);
                # TODO Duplicate full_file_path
                #Get Line Function Mapping also requires an actual file project path where the file is present. Currently that is same as the full_file_path for us.
                for line in lines:
                    if(line.attrib["hits"] == "1"):
                        number = int(line.attrib["number"])
                        if(line_function_mapping.get(number)):
                            function = line_function_mapping[number]
                            hit_function_set.add(function)
        return hit_function_set

        ## Get Changed Methods Test End

    def parse_code_coverage_and_store_in_database(self):
        '''CodeCoverageFolder is the one where the folders for all the individual test cases will be present.
        Inside the indivisual test-case folder, there will be a cobertura_output.xml file'''
        mtd = MethodTestcaseDataAccess()
        codecoverage_folder = self.workspace_folder + os.path.sep + "codecoverage"
        # Search for all files in {#codecoverage_folder} having name as cobertura_output.xml
        # Current Structure is as follows: codecoverage>module_name>testsuite_name.testcase_name. Eg. codecoverage>service>AuthenticateMgrTest.NullInitialize
        for root, dirnames, filenames in os.walk(codecoverage_folder):
            for filename in fnmatch.filter(filenames, 'cobertura_output.xml'):
                cobertura_output_file = (os.path.join(root, filename))
                methods = self.get_hit_methods_by_code_coverage(cobertura_output_file);
                for method in methods:
                    module_name = utils.get_parent_abs(root)
                    mtd.insert_method_testcase(method, os.path.basename(root), os.path.basename(module_name))