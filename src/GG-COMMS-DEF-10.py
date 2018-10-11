from genBase import (parseBxbDefStr,parseBxbDefFile,MarkdownGenerator,CcodeGenerator,OOcodeGenerator,ppprint,BaseCodeGenerator)
import os

def saveToFile(fname,s):
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    text_file = open(fname, "w")
    text_file.write(s)
    text_file.close()


def mainTest2():
    pp = parseBxbDefFile("./src/GG-comsdef-01.bxb")
    ppprint()
    docgen = MarkdownGenerator() 
    s = docgen.genAll()
    saveToFile("doc/xx.md",s)
    #print(s)
    cgen = CcodeGenerator() 
    (sh,sc) = cgen.genAll("xx.h")
    saveToFile("src_c/xx.h",sh)
    saveToFile("src_c/xx.c",sc)
    #print(s)

    cppgen = OOcodeGenerator() 
    (sh,sc) = cppgen.genAll("hh.hpp","hh.cpp")
    saveToFile("src_c/xx.hpp",sh)
    saveToFile("src_c/xx.cpp",sc)


if __name__ == "__main__":
    # execute only if run as a script
    mainTest2()