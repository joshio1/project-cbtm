from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from src.method_testcase import MethodTestcase
from src.testcase import TestCase

class MethodTestcaseDataAccess:
    '''This class is used to deal with the MethodTest objects
    Basically, performing operations to insert several method test objects and read MethodTest objects'''
    def __init__(self):
        engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/cbtm")
        Base = declarative_base()
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def insert_method_testcase(self,method,testcase, module):
        # Create objects
        try:
            mt = MethodTestcase(method_name=method.name,testcase_name=testcase,method_file=method.file,testcase_module=module, method_scope=(method.scope or "UNKNOWN"))
            #Note that default value of Scope is 'UNKNOWN". This is to overcome the mysql feature where multiple NULL values are not considered duplicate.
            #We want them to be duplicate and not allowed and hence we use 'UNKNOWN' so that they are not allowed.
            self.session.add(mt)
            self.session.commit()
        except Exception as exc:
            self.session.rollback()
            print("Problem during insertion: Message = %s"%(exc))


    def get_testcases(self,method):
        # Select objects
        testcases = []
        for mtd in self.session.query(MethodTestcase).filter(MethodTestcase.method_name == method.name, MethodTestcase.method_file == method.file, MethodTestcase.method_scope == method.scope):
            tc = TestCase(mtd.testcase_name,mtd.testcase_module)
            testcases.append(tc)
        return testcases

    def get_methods(self,testcase):
        # Select objects
        methods = []
        for mtd in  self.session.query(MethodTestcase).filter(MethodTestcase.testcase_name == testcase):
            methods.append(mtd)
        return methods