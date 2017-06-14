from code_coverage_parser.CodeCoverageParser import  CodeCoverageParser
ccp = CodeCoverageParser()
methods = ccp.get_hit_methods_by_code_coverage(r"C:\Users\joshio\CBTM\Coverage Data\Single Test CAse\codecoverage\WorkerSessionMgrTest.RecordAndValidateMapData\cobertura_output.xml");
for method in methods:
    print(method);