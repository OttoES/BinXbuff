from genBase import (parseBxbDefStr,parseBxbDefFile,MarkdownGenerator,ppprint,BaseCodeGenerator)


def mainTest2():
    pp = parseBxbDefFile("./src/GG-comsdef-01.bxb")
    ppprint()
    docgen = MarkdownGenerator() 
    s = docgen.genAll()
    print(s)
    cgen = CcodeGenerator() 
    s = cgen.genAll()
    print(s)


if __name__ == "__main__":
    # execute only if run as a script
    mainTest2()