class TestCase:
    '''Just a placeholder object. Not needed for database. i.e. no table exists specially for table.
    But required for passing around set of test-cases.'''
    def __init__(self, name, module=""):
        self.name = name
        self.module = module

    def __eq__(self, other):
        '''A method is said to be equal when its fully qualified method name(which is checked by same_as) and its content(body) are equal'''
        return self.name == other.name and self.module == other.module

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<TestCase(name='%s', module='%s')>" % (self.name, self.module)

    def __hash__(self):
        """Override the default hash behavior (that returns the id or the object)"""
        return hash(self.name) ^ hash(self.module)