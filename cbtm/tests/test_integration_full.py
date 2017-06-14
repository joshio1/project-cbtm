from unittest import TestCase
from src.runner import Runner
import os
class TestCbtm(TestCase):
    def test_end_to_end(self):
         tpg = Runner()
         one_up = os.path.abspath(os.path.join(__file__, "../.."))
         codecoverage_data_path = one_up+os.path.sep+"data"+os.path.sep+"codecoverage"
         tpg.parse_code_coverage_and_store_in_database(codecoverage_data_path)
         mtd = tpg.get_list_of_testcases_to_run_for_this_build("e015b3043b7759cf4300c2c22fdd916f8e18684f","77df49b5a4d6bbad17b4f2458a83cf5f96c08406")
         self.assertTrue(len(mtd) == 2)
         self.assertTrue(mtd[0].testcase_name == "WorkerSessionMgrTest.MultithreadedTestAPI")
         self.assertTrue(mtd[1].testcase_name == "WorkerSessionMgrTest.RecordAndValidateMapData")