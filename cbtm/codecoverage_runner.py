from src.codecoverage.codecoverage_analyzer import CodeCoverageParser
import sys
ccp = CodeCoverageParser(r"C:\Users\Administrator\workspace\appblast-ut-cbtm\build-and-ut\win7x64-ut-cbtm")
# ccp = CodeCoverageParser(sys.argv[1])
# workspace = sys.argv[1]
# Storing code coverage data into database
# ccp.parse_code_coverage_and_store_in_database(sys.argv[1])
ccp.parse_code_coverage_and_store_in_database()