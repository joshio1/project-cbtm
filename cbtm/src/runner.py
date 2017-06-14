from src.delta_fetcher import DeltaFetcher
from src.method_testcase_data_access import MethodTestcaseDataAccess
from src.codecoverage.codecoverage_analyzer import CodeCoverageParser
import os
import settings
import fnmatch
class Runner:

 def get_list_of_testcases_to_run_for_this_build(self, base_build_hash, new_build_hash, repo_folder_path=""):
     """Gets a list of test-cases to be run for this build using code coverage and code differences"""
     # df = DeltaFetcher()
     dp = DeltaFetcher(repo_folder=repo_folder_path);
     ### Get Changed Methods Test
     testcases_to_run=set()
     methods = dp.get_changed_methods_for_current_build(base_build_hash, new_build_hash);
     mtcda = MethodTestcaseDataAccess()
     for method in methods:
         tcs = mtcda.get_testcases(method)
         testcases_to_run.update(tcs)
     return testcases_to_run


