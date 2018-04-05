#!/usr/bin/python

'''
@author: Christian Hovy
'''

import os
import argparse
from Cheetah.Template import Template
from assertions import assertType, assertTypeAll

def main():
    argParser = argparse.ArgumentParser(description='Generate test code.');
    args = parseArguments(argParser);
    output = str(Template(file=args.file, searchList=[FortranGenerictorNamespace()]))
    output = alignColons(output)
    print output
    
def parseArguments(argParser):
    argParser.add_argument('file');
    return argParser.parse_args();    
    
def alignColons(code):
    lines = code.splitlines()
    firstDoubleColonLine = -1
    highestDoubleColonPosition = -1
    for i, line in enumerate(lines):
        pos = line.find('::')
        if pos >= 0:
            if firstDoubleColonLine <= 0:
                firstDoubleColonLine = i
            if pos > highestDoubleColonPosition:
                highestDoubleColonPosition = pos
        else:
            if firstDoubleColonLine >= 0:
                for j, alignLine in enumerate(lines[firstDoubleColonLine:i]):
                    pos = alignLine.find('::')
                    lines[firstDoubleColonLine + j] = alignLine.replace('::', (highestDoubleColonPosition - pos) * ' ' + '::', 1)
                firstDoubleColonLine = -1
                highestDoubleColonPosition = -1
    return os.linesep.join(lines)

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
        
    def dimensions(self, lbounds = [], ubounds = []):
        if self.__dimension.rank == 0:
            return ''
        
        lbounds = lbounds + [''] * max(self.__dimension.rank - len(lbounds), 0)
        ubounds = ubounds + [''] * max(self.__dimension.rank - len(ubounds), 0)
        
        return '(' + ','.join([lbounds[i] + ':' + ubounds[i] for i in range(0, self.__dimension.rank)]) + ')'
    
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

    def typesWithDimensions(self, excludeRanks = []):
        twds = []
        for fortranType in self.types():
            for rank in fortranType.ranks:
                if rank not in excludeRanks: 
                    twds.append(FortranTypeWithDimension(fortranType, rank))
        twds[-1].isLast = True
        return twds
    
    def unlessIsLast(self, string, element, liste):
        if liste.index(element) < len(liste) - 1:
            return string
        else:
            return ''

if __name__ == "__main__":
    main()