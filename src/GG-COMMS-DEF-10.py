from genBase import (parseBxbDefStr,parseBxbDefFile,MarkdownGenerator,CcodeGenerator,ppprint,BaseCodeGenerator,OOpythonGenerator)
from bxb2ObjCode import OOcodeGenerator
import os
    
def saveToFile(fname,s):
    os.makedirs(os.path.dirname(fname), exist_ok=True)
    text_file = open(fname, "w")    
    text_file.write(s)  
    text_file.close()   
    

def mainTest2():        
    pp = parseBxbDefFile("./src/GG-comsdef-01.bxb")
    #pp = parseBxbDefFile("./src/BXB-parser-test-01.bxb")
    ppprint()
    docgen = MarkdownGenerator() 
    s = docgen.genAll()
    saveToFile("doc/xx.md",s)   
    #print(s)
    cgen = CcodeGenerator() 
    (sh,sc,su) = cgen.genAll("xx.h")
    saveToFile("src_c/xx.h",sh)
    saveToFile("src_c/xx.c",sc)
    su = cgen.simpleReindent(su)
    saveToFile("src_c/xx_user.h",su)
    #print(s)

    cppgen = OOcodeGenerator() 
    (sh,sc) = cppgen.genAll("hh.hpp","hh.cpp")
    saveToFile("src_c/xx.hpp",sh)
    saveToFile("src_c/xx.cpp",sc)
    pygen = OOpythonGenerator() 
    s = pygen.genAll("xx.py")
    saveToFile("src_py/xx.py",s)
    
    sx = """
    void mytest() {
     for x = kkkfd {
         if fdfgf
         {
     while () {}
     if xx {

     } // if xx
         }
     }   
    } // end
    """
    s = cgen.simpleReindent(sx)
    print (s)
   

if __name__ == "__main__":
    # execute only if run as a   script
    mainTest2()