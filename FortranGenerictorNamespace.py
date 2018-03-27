from assertions import assertType, assertTypeAll

class FortranType(object):
    def __init__(self, fullname, shortname, actualDatatype, dimensions):
        self.fullname = fullname
        self.shortname = shortname
        self.datatype = actualDatatype
        self.dimensions = []
        for rank in dimensions:
            self.dimensions.append(FortranDimension(rank))

class FortranDimension(object):
    def __init__(self, rank):
        assertType(rank, 'rank', int)
        self.rank = rank

class TemplatesNameSpace(object):
    
    def __init__(self):
        self.__types = []
        self.__defaultDimensions = [0]
        
    def setDefaultDimensions(self, dimensions):
        assertType(dimensions, 'dimensions', list)
        assertTypeAll(dimensions, 'dimensions', int)
        
        self.__defaultDimensions = dimensions
    
    def addType(self, fullname, shortname, actualDatatype, dimensions = None):
        assertType(fullname, 'fullname', str)
        assertType(shortname, 'shortname', str)
        assertType(actualDatatype, 'actualDatatype', str)
        assertType(dimensions, 'dimensions', list, True)
        assertTypeAll(dimensions, 'dimensions', int, True)
        
        if dimensions is None:
            dimensions = self.__defaultDimensions
        self.__types.append(FortranType(fullname, shortname, actualDatatype, dimensions))
    
    def types(self):
        return self.__types
