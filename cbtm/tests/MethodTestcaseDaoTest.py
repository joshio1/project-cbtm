from MethodTestcaseDataAccess import MethodTestcaseDataAccess
from code_coverage_parser.CodeCoverageParser import  CodeCoverageParser
ccp = CodeCoverageParser()
mtd = MethodTestcaseDataAccess()
methods = ccp.get_hit_methods_by_code_coverage(r"C:\Users\joshio\CBTM\Coverage Data\Single Test CAse\codecoverage\WinEventCatcherTest.AddRemoveDupTest\cobertura_output.xml");
for method in methods:
    mtd.insert_method_testcase(method,"WinEventCatcherTest.AddRemoveDupTest")
# print("Inserted into method_testcase map")

# print(mtd.get_methods("WinEventCatcherTest.AddRemoveDupTest"))