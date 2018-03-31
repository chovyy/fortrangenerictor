#!/usr/bin/python

'''
@author: Christian Hovy
'''

from Cheetah.Template import Template
from assertions import assertType, assertTypeAll

def main():
    output = Template(file='m_ser_ftg.f90.cht', searchList=[FortranGenerictorNamespace()])
    print output

class FortranType(object):
    def __init__(self, name, actualDatatype, ranks):
        self.name = name
        self.datatype = actualDatatype
        self.ranks = ranks

class FortranDimension(object):
    def __init__(self, rank):
        assertType(rank, 'rank', int)
        self.rank = rank
        
class FortranTypeWithDimension(object):
    def __init__(self, fortranType, rank):
        self.__type = fortranType
        self.__dimension = FortranDimension(rank)
        self.isLast = False
        
    def name(self):
        return self.__type.name
        
    def rank(self):
        return self.__dimension.rank
        
    def datatype(self):
        return self.__type.datatype
        
    def dimension(self):
        if self.__dimension.rank == 0:
            return ''
        
        return '(' + ','.join([':'] * self.__dimension.rank) + ')'
    
    def unlessIsLast(self, string):
        if not self.isLast:
            return string
        else:
            return ''     
    
    def ifIsLast(self, string):
        if self.isLast:
            return string
        else:
            return ''     

class FortranGenerictorNamespace(object):
    
    def __init__(self):
        self.__types = []
        self.__defaultRanks = [0]
        
    def setDefaultRanks(self, ranks):
        assertType(ranks, 'ranks', list)
        assertTypeAll(ranks, 'ranks', int)
        
        self.__defaultRanks = ranks
    
    def addType(self, name, actualDatatype, ranks = None):
        assertType(name, 'name', str)
        assertType(actualDatatype, 'actualDatatype', str)
        assertType(ranks, 'ranks', list, True)
        assertTypeAll(ranks, 'ranks', int, True)
        
        if ranks is None:
            ranks = self.__defaultRanks
        self.__types.append(FortranType(name, actualDatatype, ranks))
    
    def types(self):
        return self.__types

    def typesWithDimensions(self):
        twds = []
        for fortranType in self.types():
            for rank in fortranType.ranks:
                twds.append(FortranTypeWithDimension(fortranType, rank))
        twds[-1].isLast = True
        return twds

if __name__ == "__main__":
    main()