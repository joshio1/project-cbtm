from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()

class MethodTestcase(Base):
    __tablename__ = "method_testcase"
    id = Column(Integer, primary_key=true)
    method_name = Column(NVARCHAR(100), nullable=false)
    testcase_name = Column(NVARCHAR(200), nullable=false)
    method_file = Column(NVARCHAR(300),nullable=false)
    method_scope = Column(NVARCHAR(100), nullable=false)
    testcase_module = Column(NVARCHAR(100), nullable=false)
    # explicit/composite unique constraint.  'name' is optional.
    UniqueConstraint(method_name,testcase_name, method_file, testcase_module, method_scope, name ='unique')

    def __repr__(self):
        if(self.method_scope):
            return "<Function(method_name='%s', testcse_name='%s', file='%s', module='%s', scope='%s')>" % (self.method_name, self.testcase_name, self.method_file, self.testcase_module, self.method_scope)
        else:
            return "<Function(method_name='%s', testcase_name='%s', module='%s', file='%s')>" % (self.method_name, self.testcase_name, self.testcase_module, self.method_file)

engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/cbtm")
Base.metadata.create_all(engine)