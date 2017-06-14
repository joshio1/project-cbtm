from src.delta_fetcher import DeltaFetcher
from src.method_testcase_data_access import MethodTestcaseDataAccess
from src.codecoverage.codecoverage_analyzer import CodeCoverageParser
import sys
from src.runner import Runner
import sys

tpg = Runner()

#Storing code coverage data into database
testcases =  tpg.get_list_of_testcases_to_run_for_this_build(sys.argv[2],sys.argv[3], repo_folder_path=sys.argv[1])
for testcase in testcases:
    print("%s,%s"%(testcase.name,testcase.module))

#Above printing format is very important beacuse that format is used by the batch script to run the testcases for specific modules

#Generating List of Testcases to be run
# testcases = tpg.get_list_of_testcases_to_run_for_this_build("HEAD","HEAD~100",repo_folder_path=r"C:\Users\Administrator\workspace\appblast-ut-cbtm\build-and-ut\win7x64-ut-cbtm")
# print("<------------------------- RESULT --------------------------->")
# print("Following are the high-priority test-cases for this build:")
# for testcase in testcases:
#     print("%s,%s"%(testcase.name,testcase.module))

#e015b3043b7759cf4300c2c22fdd916f8e18684f - May 31st Commit
#77df49b5a4d6bbad17b4f2458a83cf5f96c08406 - May 5th Commit
#d56da61b680793884fdd240b23490ac1f98ffb64 - June 6