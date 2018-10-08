from genBase import (parseBxbDefStr,parseBxbDefFile,MarkdownGenerator,CcodeGenerator,ppprint,BaseCodeGenerator)
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
    print(s)
    cgen = CcodeGenerator() 
    s = cgen.genAll()
    saveToFile("src_c/xx.c",s)
    print(s)


if __name__ == "__main__":
    # execute only if run as a script
    mainTest2()