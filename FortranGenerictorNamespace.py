from assertions import assertType, assertTypeAll

class FortranType(object):
    def __init__(self, fullname, shortname, actualDatatype, ranks):
        self.fullname = fullname
        self.shortname = shortname
        self.datatype = actualDatatype
        self.ranks = ranks

class FortranDimension(object):
    def __init__(self, rank):
        assertType(rank, 'rank', int)
        self.rank = rank
        
class FortranTypeWithDimension(object):
    def __init__(self, fortranType, rank):
        self.__type = fortranType
        self.__dimension = fortranType.dimensions[rank]

class TemplatesNameSpace(object):
    
    def __init__(self):
        self.__types = []
        self.__defaultRanks = [0]
        
    def setDefaultRanks(self, ranks):
        assertType(ranks, 'ranks', list)
        assertTypeAll(ranks, 'ranks', int)
        
        self.__defaultRanks = ranks
    
    def addType(self, fullname, shortname, actualDatatype, ranks = None):
        assertType(fullname, 'fullname', str)
        assertType(shortname, 'shortname', str)
        assertType(actualDatatype, 'actualDatatype', str)
        assertType(ranks, 'ranks', list, True)
        assertTypeAll(ranks, 'ranks', int, True)
        
        if ranks is None:
            ranks = self.__defaultRanks
        self.__types.append(FortranType(fullname, shortname, actualDatatype, ranks))
    
    def types(self):
        return self.__types

    def typesWithDimension(self):
        twds = []
        for fortranType in self.types():
            for rank in fortranType.ranks:
                twds.append(FortranTypeWithDimension(fortranType, rank))
        return twds