""" Copyright OttoES 2018
"""

from parseBinXbuff import (parser, enumList  , structList,structDict, msgList,msgDict, annotateDict)

from pprint import pprint

import re

def cleanstr(s):
    if s.startswith("'''"):  s = s[3:-3]
    if s.startswith('/*'):  s = s[2:-2]
    if s.startswith('"'):  s = s[1:-1]
    #if s.endswith('*/'):  s = s[2:]
    return s

def cleanstrNL(s):
    return s.replace("\n", " ")

def addIndent(s):
    if s.find("\n") < 2:  # start with new line
        return s.replace("\n", "\n   ")
    s = "    " + s.replace("\n", "\n   ")
    return s
    
def parseBxbDefFile(fileName):
    parser.parseFile(fileName)
    # docgen = MarkdownGenerator() 
    # s = docgen.genAll()
    # print(s)


def parseBxbDefStr(defStr):
    parser.parseString(defStr)
    docgen = MarkdownGenerator() 
    s = docgen.genAll()
    print(s)

def ppprint():
    pprint(enumList)
    pprint(annotateDict)
    pprint(structList)


class BaseCodeGenerator:
    codeHeader          = " Auto generated code"
    codeCommentStart    = "/* "
    codeCommentEnd      = " */"
    codeCommentLineStart= "// "
    doxPre              = "\n @"         # doxygen prefix
    doxPost             = " "         # doxygen prefix
    typePostfix         = "_t"
    funcNamePrefix      = "BIN_"
    funcPackCallPrefix  = "BIN_call"
    funcPackBaseName    = "packMsg"
    funcUnpackBaseName  = "unpackMsg"
    funcCreateName      = "objFactory"
    funcCreateFromBufName= "objFactory"
    funcProcessBuffName = "CallStoreSendBuffer"
    funcUnpackNamePrefix= "BIN_unpack"
    funcProcessFunPrefix= "BIN_process"              # prefix for the functions that process incoming messages
    noTypeName          = "void" 
    intTypeName         = "int "
    lenTypeName         = "size_t "                  # buffere length etc
    singletonFuncDecl   = "\n// singleton function\n"# will be static if in a class
    privateFuncDecl     = "static "                  # will be private if in a class
    errorHandlerName    = "printf"                   # function that will be called on an error  
    constErrBuffOutOfBounds = "ERR_BUFF_OUT_OF_BOUNDS"
    constErrBuffShort   = "ERR_BUFF_OUT_OF_DATA"
    constErrUnknownTag  = "ERR_TAG_UNKNOWN"
    constErrCRC         = "ERR_CRC_FAIL"
    typeTable1          = {"bool":"bool","enum8":"uint8_t","char":"char"}
    typeTable2          = {"string":"char","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    # these types are internally generated and not passed in by the user  
    typeTableLoc        = {"CRC8":"uint8","CRC16":"uint16","CRC32":"uin32","MSG_ID16":"uint16"}
    typeSizeTable       = {"char":1,"bool":1,"wchar":2,"byte":1}
    packBuffName        = "buff"  
    packBuffType        = "char"
    # define the languages (use the file extension)
    LANG_C              = "c"  
    LANG_CPP            = "cpp"  
    LANG_PY             = "py"  
    LANG_JAVA           = "java"  
    def __init__(self,bxbDef= None):
        if bxbDef is not None:
            pp = parser.parseString(bbxDef)
        # set the language
        self.LANG = "?"
    def pprint(self):
        pprint(enumList)
        pprint(structList)
    def lookupType(self,vartype):  
        if vartype in self.typeTable2: return  self.typeTable2[vartype]
        if vartype in self.typeTable1: return  self.typeTable1[vartype]
        return vartype+self.typePostfix          
    def lookupTypeSize(self,vartype):  
        # handel all the non standard cases that is in the table
        if vartype in self.typeSizeTable: return  self.typeSizeTable[vartype]
        # do the standard cases where the bit isze is embedded in the type name
        if vartype.find("8") >0 : return 1
        if vartype.find("16")>0 : return 2
        if vartype.find("32")>0 : return 4
        if vartype.find("64")>0 : return 8
        return -100000  # this is an n error
    def getParent(self,structt):
        if not "parentName" in structt: return None 
        parnt = structt["parentName"]
        return structDict[parnt]  
    def makeConsVarDecl(self,varType,varName,varVal):
        #tt = self.lookupType(varType)
        return "static const " + varType + " "+varName  + " = ("+varType+") ("+varVal+  ");"
    def makeVarDecl(self,varType,varName,arrayLen = None):
        return genVarOnlyDecl(self,varType,varName,arrayLen = None)

    def genVarOnlyDecl(self,varType,varName,arrayLen = None):
        ''' Generate variable declaration of the given type.
            If an array size given it will be declared as an 
            array of that size.
            Note that arrayLen of 0 is handeled differently:
            it will be declared as an array argument using "[]"
            as normally used in function arguments.
        '''
        tt = self.lookupType(varType)
        s  = tt + " "+varName
        if arrayLen is not None:
            if arrayLen == 0:
                s += "[]"
            else:
                s += "[" + str(arrayLen) +"]"
        return s
    def isMessage(self,structt):
        if self.findInConstList( structt,"MSG_ID"): return True
        if self.findInConstList( structt,"MSG_COND"): return True
        return False
    def isStruct(self,structt):
        if self.findInConstList( structt,"STRUCT"): return True
        return False
    def genFileHeader(self,fileName):
        s  = self.codeCommentStart
        s += "--Autogenerated code--\n"
        s += "File name : "+fileName + "\n"
        if "name" in annotateDict:
            s += "Name      : "+cleanstr(annotateDict["name"]) + "\n"
        if "version" in annotateDict:
            s += "Version   : " + cleanstr(annotateDict["version"]) + "\n"   
        if "copyright" in annotateDict:
            s += "Copyright : " + cleanstr(annotateDict["copyright"]) + "\n"   
        return s + self.codeCommentEnd + "\n"
    def genPackVar(self,buff,buffpos,vartype,varname, varval): 
        #if vartype in self.typeTable2: 
        #    return self.funcPackNamePrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
        return self.funcPackCallPrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
    def genArg(self,fields):    
        s = ""
        for f in fields:
            s = s + f["name"] + ","
        return s[:-1] 
    def genTypedArg(self,fields):    
        s = ""
        for f in fields:
            # if the field is in the locked list it is internally 
            # generated and should not be in the argument list so skip it
            if f["type"] in self.typeTableLoc: 
                continue
            if "arrLen" in f:
                # 0 will force it to use [] in declaration
                arrLen = 0   
            else:
                arrLen = None
            #arrLen = f.get("arrLen",None)    
            s += self.genVarOnlyDecl(f["type"] , f["name"],arrLen ) + ","
            #s = s + self.lookupType(f["type"])+ "  "+ f["name"] + ","
        return s[:-1] 
    #####-------------------------------------
    def makeFunName(self,structt,retType,funName,args,isSingletonFun = False,isPrivate = False):
        """ Make a valid function declaration

        Arg:
          funName    - the base name (root) of the name. If it is part of a class
                       it should be prefixed wih the class name (or what ever the 
                       programming language require)
          args       - function arguments
          isSingletonFun  specifies wether it is a static class member 
          isPrivate       means that it will not be called externally
        """
        s = ""
        if isPrivate:      s+= self.privateFuncDecl
        if isSingletonFun: s+= self.singletonFuncDecl
        nn = structt['name'].upper() + "_" + funName
        s += retType + " " + nn + "(" + args + ")"
        return s
    def makeDeclFunArgList(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = "," , inclParent = True , inclConst = False, inclPrivate = False )    
    def makeCallFunArgList(self,structt):
        return self.makeFieldListGeneric(structt,False, seperator = "," , inclParent = True , inclConst = False, inclPrivate = False )
    def makeCallFunArgListAll(self,structt):
        return self.makeFieldListGeneric(structt,False, seperator = "," , inclParent = True , inclConst = True )
    def makeClassMemberList(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = ";\n  " , inclParent = False , inclConst = True )
    def makeFieldListGeneric(self,structt,inclTypes, seperator = "," , inclParent = True , inclConst = False, noLastSeparater = True, inclArrLen =False, inclPrivate = False ):
        """ Flexible generation of variable/argument list 
        """
        fields    = structt["body"]
        s = ""
        if inclParent and "parentName" in structt:
            parnt = self.getParent(structt)
            s += self.makeFieldListGeneric(parnt,inclTypes, seperator, inclParent , inclConst,inclArrLen = inclArrLen) + seperator
        for f in fields:
            # if the field is assigned a value 
            # do not include in the argument list 
            # but can be over ridden with  inclConst
            if "value" in f and inclConst == False: 
                continue  
            if inclPrivate == False and f["name"].startswith("__"):
                continue            
            arrLen = f.get("arrLen",None)    
            if inclTypes:
                #s += self.genVarDecl(f["type"] , f["name"],arrLen ) + seperator
                s += self.genVarDecl(f, inclArrLen = inclArrLen, termstr = seperator ) 
            else: 
                #s += self.genVarOnlyDecl(f["type"] , f["name"],arrLen ) + seperator
                s += f["name"] + seperator
        if  noLastSeparater: 
            return s[:-len(seperator)]
        return s         
    def genPackLenCalc(self,structt):    
        # calculate the struct size by finding the last field offset
        lastField = structt["body"][-1]        
        return self.genPackFieldPosCalc(structt,lastField,True)
          
    ## try to simplify the equation if it only contains numbers
    def simplifyEq(self,eqs):    
        if any(c not in '0123456789+*- ' for c in eqs):  
            return eqs,False
        ll = eval(eqs)
        return ll,True
    def genVarDecl(self,sfield,inclArrLen =False, termstr = ";", setInitValue = True):
        if not "type" in sfield:
            return "" 
        vtype = sfield["type"]
        vname = sfield["name"]
        if vtype in self.typeTable2: 
            s = self.lookupType(vtype) +" "+vname+"["+sfield["type"]+"]"
        else:  
            s = self.lookupType(vtype) +" "+vname
        if 'arrLen' in sfield:
            if inclArrLen:  
                s = s +"["+sfield['arrLen']+"]"
            else:
                s = s +"[]"
        if 'value' in sfield:
            if setInitValue:
                s = s + " = " +  sfield["value"]
        s = s + termstr   
        return s
    def findInConstList(self,lst,sstr):
        for itm in lst:
            if itm['name'] == sstr: return itm
        return None
    def isAnnoTagDefined(self,structt,annostr):
        """Check if the annotation is present for this structure
        """
        if "anno" in structt:
                lst     = structt["anno"]
                anno = self.findInConstList(lst,annostr)
                if anno: return True
        return False
    def oldisFuncRequired(self,structt,funct,lang):
        """Check if this function should be generated.

           More or less the following logic:
              - look at struct annottion
              - look at global language anotation
              - look at global annottion
        """
        # local annoation takes precedence so first look at that
        if "anno" in structt:
            lst     = structt["anno"]
            anno = self.findInConstList(lst,lang+"_"+funct)
            if anno: return True
            anno = self.findInConstList(lst,lang+"_"+funct+"_FALSE")
            if anno: return False
            anno = self.findInConstList(lst,funct)
            if anno: return True
            anno = self.findInConstList(lst,funct+"_FALSE")
            if anno: return False
        lst     = annotateDict
        if lang+"_"+funct in lst:
            return True
        if lang+"_"+funct+"_FALSE" in lst:
            return False
        if funct in lst:
            return True
        if funct+"_FALSE" in lst:
            return False
        return True

    def getLocalAnno(self,structt,annotag,default=None):
        """Find the relevant annotation if available otherwise assume a default.

           More or less the following logic:
              - look at struct annotation for this language
              - look at struct annotation
              - look at global language annotation
              - look at global annottion
        """
        # this is the language spesific annotation tag that will overrride the general annotation
        lannotag = self.LANG +"_"+annotag
        # local struct annotation takes precedence, so first look at that
        if "anno" in structt:
            lst     = structt["anno"]
            anno = self.findInConstList(lst,lannotag)
            if anno: 
                if "value" in anno:
                    return anno['value']
                if "string" in anno:
                    return anno['string']
            anno = self.findInConstList(lst,annotag)
            if anno: return anno['value']
        lst     = annotateDict
        if lannotag in lst:
            return lst[lannotag]
        if annotag in lst:
            return lst[annotag]
        return default

    # ==================================================

class CcodeGenerator(BaseCodeGenerator):
    def __init__(self):
        # set the language
        self.LANG = BaseCodeGenerator.LANG_C
    def genPackFieldCode(self,f):
        tsize = self.lookupTypeSize(f["type"])
        if "arrLen" in f:  
            lenstr = str(tsize)+"*" + f["arrLen"]
            ## this is only valid if the endianess is the same for multibyte types !!!!
            return "memcpy("+self.packBuffName+","+f["name"] +","+lenstr + ");\n"
        if tsize == 1:
            return self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
        elif tsize == 2: 
            # this is stored in little endian
            s = self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
            return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>8);\n"
        elif tsize == 4: 
            # this is stored in little endian
            s  = self.makeLineComment(" it is faster to copy byte by byte than calling memcpy()")
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>8);\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>16);\n"
            return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>24);\n"
        s  = "pos    += " + self.funcPackCallPrefix + f["type"].capitalize() 
        s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s
    def genUnpackFieldCode(self,f):
        tsize   = self.lookupTypeSize(f["type"])
        bufname = self.packBuffName 
        if "arrLen" in f:  
            lenstr = str(tsize)+"*" + f["arrLen"]
            ## this is only valid if the endianess is the same for multibyte types !!!!
            return "memcpy("+f["name"] +","+bufname+","+lenstr + ");\n"
        if tsize == 1:
            return f["name"] + " = ("+f["type"]+ ")" + bufname+"[pos++] " + ";\n"
        elif tsize == 2: 
            # this is  little endian
            return f["name"] + " = ("+ self.lookupType(f["type"])+ ")(" + bufname+"[pos] + ("  + bufname+"[pos+1]<<8)" +  ");\npos +=2;\n"

        elif tsize == 4: 
            # # this is stored in little endian
            # s  = "// it is faster to copy byte by byte than calling memcpy()\n"
            # s += "    "+ self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
            # s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>8);\n"
            # s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>16);\n"
            # return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+ f["name"] + ">>24);\n"
            # this is  little endian
            return f["name"] + " = ("+ self.lookupType(f["type"])+ ")(" + bufname+"[pos] + ("  + bufname+"[pos+1]<<8) + (((uint32_t)"+ bufname+"[pos+2])<<16) + (((uint32_t)"+ bufname+"[pos+3])<<24)) " +  ");\npos +=4;\n"
        s  = "pos    += " + self.funcPackCallPrefix + f["type"].capitalize() 
        s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s
    
    def genPackFields(self,structt):    
        fields    = structt["body"]
        s = ""
        for f in fields:
            if f["type"] == "CRC16":
              p1,fnd1 = self.genPackFieldPosCalc(structt,f['rangeStart'],False)
              p2,fnd2 = self.genPackFieldPosCalc(structt,f['rangeEnd'],True)
              s += "    int16_t   "+f["name"] +" += CalcCRC16"+f["name"]+"("+self.packBuffName+", "+p1 + "," + p2 + ");\n" 
            #-- check if it is assigned a value
            if "value" in f:
                s += "    "+self.makeLineComment(" this is a fixed assigned field")
                #s += "    " + f["name"] +" = " + f["value"] +";\n" 
                s += "    " + self.makeConsVarDecl(f["type"],f["name"],f["value"]) +"\n"
            s += "    " + self.genPackFieldCode(f) 
            #s += "    pos    += " + self.funcPackNamePrefix + f["type"].capitalize() 
            #s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s 
    def genUnpackFields(self,structt):    
        fields    = structt["body"]
        s = ""
        for f in fields:
            if f["type"] == "CRC16":
              p1,fnd1 = self.genPackFieldPosCalc(structt,f['rangeStart'],False)
              p2,fnd2 = self.genPackFieldPosCalc(structt,f['rangeEnd'],True)
              s += "    ??int16_t   "+f["name"] +" += CalcCRC16"+f["name"]+"("+self.packBuffName+", "+p1 + "," + p2 + ");\n" 
            #-- check if it is assigned a value
            if "value" in f:
                s += "    "+self.makeLineComment(" this is a fixed assigned field")
                s += "    " + self.makeConsVarDecl(f["type"],f["name"],f["value"]) +"\n"
            s += "    " + self.genUnpackFieldCode(f) 
            #s += "    pos    += " + self.funcPackNamePrefix + f["type"].capitalize() 
            #s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s 
    # includeField inidcate if the field named fieldName shold be included in the position calculations    
    #def genPackFieldPosCalc(self,fields,fieldName,includeField):    
    def genPackFieldPosCalc(self,structt,fieldName,includeField):    
        fields    = structt["body"]
        ##fieldName = structt['name']
        s = ""
        if "parentName" in structt:
            parnt = structt["parentName"]
            parStruct = structDict[parnt]
            s,fieldFound = self.genPackFieldPosCalc(parStruct,fieldName,includeField)
            if fieldFound: return s,True
            if s != "":  s += "+ "
        for f in fields:
            # if the selected field size must be included
            if includeField == False:    
                if f["name"] == fieldName: 
                    if len(s) < 1: return "0",True  # if it is the first element
                    return s[:-1],True
            # if it is an array, multiply with the array length        
            if 'arrLen' in f: 
                s = s +" ("+f['arrLen']+")*"
            # get the size of the element
            s += str(self.lookupTypeSize(f["type"]))+ "+"
            if f["name"] == fieldName: 
                return s[:-1],True
        return s[:-1],False
    def genCreateFunDecl(self,structt,copyToBuff=True,msgIdArg = False,namePrefix = ""):
        args  = "void"
        s     = self.makeFunName(structt,structt['name'],namePrefix+self.funcCreateName,args)
        return s
    def genCreateFromBuffFunDecl(self,structt,copyToBuff=True,msgIdArg = False,namePrefix = ""):
        args  = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" len "
        s     = self.makeFunName(structt,structt['name'],namePrefix+self.funcCreateFromBufName,args)
        return s
    def genUnpackFunDecl(self,structt,copyToBuff=True,msgIdArg = False,namePrefix = ""):
        args  = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" len "
        s     = self.makeFunName(structt,self.intTypeName,namePrefix+self.funcUnpackBaseName,args)
        return s
    def genPackFunDecl(self,structt,copyToBuff=True,msgIdArg = False,namePrefix = ""):
        structnme     = structt["name"]
        fields        = structt["body"]
        parentArgs    = ""
        s  = "\n"
        # generate the comments
        s += self.codeCommentStart
        s += self.doxPre + "param buff[]"+self.doxPost+"    buffer into which data should be packed "
        s += self.doxPre + "param pos"+self.doxPost+"       start position in buffer "
        s += self.doxPre + "return if > 0"+self.doxPost+"   position in array of last extracted data"
        s += self.doxPre + "return if < 0"+self.doxPost+"   error in data stream "
        s += "\n" + self.codeCommentEnd +"\n"
        #-- build the argument list for the function
        if copyToBuff:
            args = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" pos, "
        else: args = ""
        args += self.makeDeclFunArgList(structt)
        #-- build the function call
        s += self.makeFunName(structt,self.intTypeName,namePrefix+self.funcPackBaseName,args)
        return s
    def genPackFun(self,structt,msgIdArg = False,namePrefix = ""):
        # determine if the function should be defined 
        #if not self.isFuncRequired(structt,"pack",self.LANG) : return ""
        ret = self.getLocalAnno(structt,"pack","TRUE")
        if ret == "FALSE" : return ""    # function should not be generated
        # determine if a function call in pack is defined
        callFuncName  = self.getLocalAnno(structt,"call_in_pack","FALSE")
        copyToBuff    = (ret == "FALSE")
        structnme     = structt["name"]
        fields        = structt["body"]
        parentArgs    = ""
        s  = self.genPackFunDecl(structt,copyToBuff=copyToBuff,msgIdArg = msgIdArg,namePrefix = namePrefix)
        s += "\n{\n"
        #-- generate constant declaraions for the struct local constant assignments
        locConst = structt.get("localConst",[])    
        for itm in locConst:
            valexp = itm.get("value","")+itm.get("expr","")
            s1 = self.makeConsVarDecl(self.intTypeName,itm["name"],valexp)
            s +=  "    "+ (s1) +"\n"
        #-- calculate the length of the data
        (structLen,__) = self.genPackLenCalc(structt)
        s += "    const "+self.intTypeName +" "+self.packBuffName+"Len = " + structLen
        #s += "    const int "+self.packBuffName+"Len = " + self.genPackLenCalc(fields)
        s += ";\n"
        if not copyToBuff:
            s += "          "+self.intTypeName +" pos    = 0;\n"
            s += "    uint8_t   "+self.packBuffName+"["+self.packBuffName+"Len];\n"
        #s += self.makeClassMemberList(structt)
        else:
            s += "    if ("+self.packBuffName+"Len > bufSize) return "+self.constErrBuffShort+";   "+self.makeLineComment("buffer to small")
        if "parentName" in structt:
            # fill in the inherited data from the parent
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            #parentStruct  = parentStruct["body"]
            s += self.genPackFields(parentStruct)
            #parentArgs    = self.genTypedArg(parentStruct) +", "            s += "    pos = " +self.funcPackBaseName + structt["parentName"].capitalize() 
            #s += "(" + self.packBuffName + ", pos, "+ self.genArg(parentStruct) +");\n"

        # for name,val in locConst.items():
        #     s += self.makeConsVarDecl("int",name,value)
        #-- build the assignment of the data fields to the buffer
        s += self.genPackFields(structt)
        # see if a custom funcion call defined 
        if not copyToBuff:
            s += "    return  "+self.funcProcessBuffName+"("+self.packBuffName
            s += ", pos);\n"
        else:
            s += "    return  pos;\n"
        s += "\n} // end\n"
        return s
    def genUnpackFun(self,structt,callParentUnpack=False,msgIdArg = False,namePrefix = ""):
        # determine if the function should be defined 
        ret = self.getLocalAnno(structt,"unpack","TRUE")
        if ret == "FALSE" : return ""    # function should not be generated
        structnme     = structt["name"]
        fields        = structt["body"]
        parentArgs    = ""
        s  = self.genUnpackFunDecl(structt,msgIdArg = msgIdArg,namePrefix = namePrefix)
        s += "\n{\n"
        s += "    "+self.intTypeName +" pos = 0;\n"
        #s += "    const int "+self.packBuffName+"Len = " + self.genPackLenCalc(fields)
        #s += ";\n"
        if "parentName" in structt:
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            if callParentUnpack:
                #s += "   pos += "+self.genUnpackFun(parentStruct,callParentUnpack=callParentUnpack,namePrefix = namePrefix) +";\n"
                funname = prn+"::"+self.funcUnpackBaseName
                s += "    pos += "+self.makeFunName(structt,"",funname,args = "buff,pos") + ";\n"
            else:
                #s += "    if ("+self.packBuffName+"Len > bufSize) return 0;   // buffer to small\n"
                s += self.genUnpackFields(parentStruct)

        #-- build the assignment of the data fields to the buffer
        s += self.genUnpackFields(structt)
        # if not copyToBuff:
        #     s += "    return  "+self.funcProcessBuffName+"("+self.packBuffName
        #     s += ", pos);\n"
        # else:
        #     s += "    return  pos;\n"
        s += "\n} // end\n"
        return s

    def genEnumStart(self,enm):
        return  "\ntypedef enum "+enm["enumName"] + " {"
    def genEnumEnd(self,enm):
        return  "} "+enm["enumName"] + self.typePostfix +";\n"  


    def genAllEnumDefs(self,separator = ","):    
        s = ""
        lastSeperator = len(s)
        for enm in enumList:
            s += self.genEnumStart(enm) + "\n"
            #s += "\ntypedef enum "+enm["enumName"] + " {\n"
            elmlist = enm["values"]
            for vv in elmlist:
                s += "  "+vv["name"].ljust(20) +" = "+ vv["value"].ljust(4)+separator
                lastSeperator = len(s)
                if "comment2" in vv:
                  s += "    " + self.codeCommentLineStart + vv["comment2"]
                s += "\n"
            # remove the comma after the last enum
            if lastSeperator > 4:
                s = s[:lastSeperator-1] + ' ' + s[lastSeperator:] 
            s += self.genEnumEnd(enm) + "\n"
            #s += "} "+enm["enumName"] + self.typePostfix +";\n"  
        return s + "\n"
    # def genHeader(self,pp):
    #     s = "*Autogenerated code\n"
    #     if  "comment" in pp:
    #       s += pp["comment"]
    #     return s

    def genProcessMsgDetail(self,structt):
        s  = "      "+self.makeLineComment( "unpack each field into a variable")
         #s += self.genVarDecl(sfield,inclArrLen =False, termstr = ";")
        s += "      " + self.makeFieldListGeneric(structt,inclTypes = True, seperator = ";\n      " , inclParent = False , inclConst = False,  noLastSeparater = False ,inclArrLen =True )
        s1 = ""
        for f in  structt["body"]:
           s1 += self.genUnpackFieldCode(f)
        s  += s1.replace("\n","\n      ")
        s += "if (pos > len) "
        s += "   {\n        // error\n        "+self.errorHandlerName+'("Message '+structt['name']+' to short");\n        return -2;\n      }\n'
        s += "      "+ self.makeLineComment("call the (external user) defined function with the unpacked data")
        s += "      "+ self.funcProcessFunPrefix + structt["name"] +"("
        s += self.makeCallFunArgListAll(structt)
        s += ");\n"
        return s

    def genProcessMsgFuns(self):
        #find the base messages
        s = ""
        for st in structList:
            if "localConst" in st:
                lst     = st["localConst"]
                bstruct = self.findInConstList(lst,"MSG_BASE")
                # if MSG_BASE is declared, a message select and unpack is created
                if bstruct :
                    s += self.genSelecAndProcessMsgFun(st)            
        return s

    def genSelecAndProcessMsgFun(self,baseStructt):
        s  = "\n// This is the base message parser that should be called with\n// the byte array to be translated to a spesific message\n"
        s  = "// First determine the struct/message type based on MSG_ID and\n// MSG_COND and then unpack\n"
        #s += self.singletonFuncDecl + self.lenTypeName + " " + "parseMsg(uint8_t buff[],int len) \n{\n"
        s += self.makeFunName(baseStructt,self.intTypeName,self.funcUnpackNamePrefix, "uint8_t buff[],int len",isSingletonFun=True) + "\n{\n"
        #s += self.genVarDecl(sfield,inclArrLen =False, termstr = ";")
        s += "   " + self.makeFieldListGeneric(baseStructt,inclTypes = True, seperator = ";\n   " , inclParent = False , inclConst = False,  noLastSeparater = False ,inclArrLen =True)
        s1 = ""
        for f in  baseStructt["body"]:
           s1 += self.genUnpackFieldCode(f)
        s  += s1.replace("\n","\n   ")
        s += "\n"
        for st in structList:
            if "localConst" in st:
                lst = st["localConst"]
                s1  = ""
                s2  = ""
                itm = self.findInConstList(lst,"MSG_ID")
                if itm :
                    if 'expr' in itm:
                        s1 = "(msg_id == "+itm['expr']+")"
                    elif 'value' in itm:
                        s1 = "(msg_id == "+itm['value']+")"
                itm = self.findInConstList(lst,"MSG_COND")
                if itm :
                    if 'expr' in itm:
                        s2 = "("+itm['expr']+")"
                if len(s1)>1 and len(s2)>1:
                    s3 = "   if ("+s1+" & "+s2+") {\n"
                else: 
                    s3 = "   if "+s1+s2+" {    // "+ st["name"] + "\n"
                if len(s1)>1 or len(s2)>1:
                    s += s3+ self.genProcessMsgDetail(st)
                    s += "   } else \n"
            #s += self.genPackFun( st) +"\n"
        s += "   {\n      // error\n      "+self.errorHandlerName+'("Unknown message tag");\n      return -1;\n   }\n'
        s += "   return pos;\n"
        s += "} // end\n"
        return s

    def makeLineComment(self,comment):
        return self.codeCommentLineStart + comment +"\n"
    def makeLineCommentDivider(self):
        return self.makeLineComment("---------------------------------------")
    def makeLineCommentDivider2(self):
        return self.makeLineComment("=======================================")
    def makeConstDecl(self,vname,vval):
        return "#define " + vname.ljust(15) + " " +vval+ "\n"
    def genAuxDef(self):
        s  = self.makeLineComment(" Constant return values defined")
        s += self.makeConstDecl(self.constErrBuffOutOfBounds,"-2")
        s += self.makeConstDecl(self.constErrBuffShort,"-4")
        s += self.makeConstDecl(self.constErrUnknownTag,"-6")
        s += self.makeConstDecl(self.constErrCRC,"-23")
        return s + "\n"
    def genStructVarDecls(self,structt):
        # for each field, add a declaration
        s  = ""  
        for f in structt["body"]:
            if 'value' in f:
              vv = f["value"]
            else:
              vv = None
            s += "  "+self.genVarDecl(f, termstr = ";\n",setInitValue = False)
            #s += "  "+self.genVarDecl(f["type"],f["name"],vv, termstr = ";\n")
        return s   
    def genStructDeclBegin(self,structname,parentstruct= None):
        
        s  = "typedef struct "+structname+" {\n"
        if parentstruct is not None: 
            s += "  " + parentstruct['name'] + " ??;\n"
        #s += "{\n \n"
        return s
    def genStructDeclEnd(self,structname):
        s = "} "+structname+ self.typePostfix + ";\n\n"
        return s
    def isStructDeclUsed(self,structt):
        return self.isAnnoTagDefined(structt,'STRUCT')
    def genCstructs(self):
        s  = ""
        for st in structList:
          if self.isStructDeclUsed(st):
            s += self.genStructDeclBegin(st['name'])
            s += self.genStructVarDecls(st)
            s += self.genStructDeclEnd(st['name'])
        return s
    def genFuncPrototypes(self):
        s  = ""
        for structt in structList:
            s += self.makeLineComment("@param buff[]    buffer with data to be unpacked ")
            s += self.makeLineComment("@param len       number of bytes in buff, must be at long enough for complete struct ")
            s += self.makeLineComment("@return if > 0 : position in array of last extracted data")
            s += self.makeLineComment("@return if < 0 : error in data stream (-4: too short, -23: CRC error")
            #nn = structt['name'].upper() + "_"
            nn = ""
            s += self.genUnpackFunDecl(structt,namePrefix = nn ) #,msgIdArg = msgIdArg,namePrefix = namePrefix)
            s += ";\n"
            s += self.genPackFunDecl(structt,namePrefix = nn)
            s += ";\n"
            
            #s += self.genStructDeclBegin(st['name'])
            #s += self.genStructVarDecls(st)
            #s += self.genStructDeclEnd(st['name'])
        return s

    def genAll(self,hfilename,cfilename= "xxxx.c"):
        sh  = ""
        sh += self.genFileHeader(hfilename)
        hprot = "__"+hfilename.upper().replace(".","_").replace("/","_") +"__"
        sh += "#ifndef "+hprot +"\n"
        sh += "#define "+hprot +"\n"
        sh += annotateDict.get('c_includes',"")
        sh += self.genAuxDef()
        sh += self.makeLineCommentDivider()
        sh += self.genAllEnumDefs()
        sh += self.genCstructs()
        sh += self.makeLineCommentDivider()
        sh += self.makeLineComment("Function declarations")
        sh += self.makeLineCommentDivider()
        sh += self.genFuncPrototypes()
        sh += "#endif  // "+hprot +"\n"
        
        sc  = "// C code \n"
        sc += '#include "'+hfilename +"\n"
        sc += annotateDict.get('c_includes',"")
        sc += annotateDict.get('c_code',"")
        for st in structList:
            sc += self.genPackFun( st) +"\n"
            sc += self.genUnpackFun( st) +"\n"
        sc += self.genProcessMsgFuns()
        return sh,sc


class OOcodeGenerator(CcodeGenerator):
    typeTable1      = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
    def __init__(self):
        # set the language
        self.LANG = BaseCodeGenerator.LANG_CPP
    def genClassDeclBegin(self,structname,parentstruct= None):
        s = "class "+structname+" "
        if parentstruct is not None: 
            s += ": public " + parentstruct + "\n"
        s += "{\n public:\n"
        return s
    def genClassDeclEnd(self,structname):
        s = "}; // end class "+structname+ "\n\n"
        return s

    def genClassDef(self,struct):
        parent = struct.get("parentName",None)
        s  = self.genClassDeclBegin(struct["name"],parent) 
        #  for each field, add a declaration
        s += self.genStructVarDecls(struct)
        # for f in struct["body"]:
        #     if 'value' in f:
        #       vv = f["value"]
        #     else:
        #       vv = None
        #     s += "  "+self.genVarDecl(f, termstr = ";\n")
        #     #s += "  "+self.genVarDecl(f["type"],f["name"],vv, termstr = ";\n")
        # generate the serialze and deserialize functions for the struct
        s1 = self.genCreateFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.genCreateFromBuffFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.genPackFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.genUnpackFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s += self.genClassDeclEnd(struct["name"])
        return s
    def genClassImplementation(self,struct):
        parent = struct.get("parentName",None)
        s  = self.makeLineCommentDivider2()
        s += self.makeLineComment( "Class "+struct["name"] + " implementation")
        s += self.makeLineCommentDivider()
        # generate the serialze and deserialize functions for the struct
        s += self.genPackFun(struct,namePrefix = struct['name']+"::")
        s += self.genUnpackFun(struct,namePrefix = struct['name']+"::",callParentUnpack=True)
        #s += "  "+addIndent(s1) + "\n"
        return s
    def genAll(self,hFileName,cFileNme):
        # generate h file -------
        s  = self.codeCommentStart + "\n" + self.genFileHeader(hFileName)
        s += self.codeCommentEnd + "\n"
        s += annotateDict.get('copyrigh',"")
        s += annotateDict.get('h_includes',"")
        s += self.genAllEnumDefs()
        s += self.genAuxDef()
        for st in structList:
            s += self.genClassDef( st) +"\n"

        # generate cpp file -------
        ss = '#include "' + hFileName + "\n"
        ss += annotateDict.get('c_includes',"")
        ss += annotateDict.get('c_code',"")
        for st in structList:
            ss += self.genClassImplementation( st) +"\n"
        return s,ss

# generate documentation
class MarkdownGenerator(CcodeGenerator):
    H1     = "\n# "
    H2     = "\n## "
    H3     = "\n### "
    LIST   = "* "
    BOLT   = "**"
    LINE   = "___\n"
    DLINE  = "___\n___\n"
    NLNL   = "\n"
    BR     = "\n\n"
    COL    = "|"
    ROW    = "\n|"
    def genInternalLink(m,ltext,linktag=None):
        if linktag is None: linktag= ltext
        #if ltext in enumList:
        #   s ="["+ltext+"](#"+"enum-" + ltext.lower() +")"
        #elif ltext in structList:  
        s ="["+ltext+"](#" + linktag.lower() +")"
        return s
    # def checkForLink(m,ltext):
    #     # search through the ext o see if there are any 
    #     #if ltext in enumList:
    #     #   s ="["+ltext+"](#"+"enum-" + ltext.lower() +")"
    #     #elif ltext in structList:  
    #     s ="["+ltext+"](#" + linktag.lower() +")"
    #     return s
    def genDocEnums(m):
        s  = m.H2 + "Enumerations\n" + m.LINE
        for enm in enumList:
            s += m.H3 + "Enum " + enm["enumName"] +"\n"
            if "comment" in enm:
                s += cleanstr(enm["comment"]) +m.NLNL
            # if "parentName" in st:
            #     s += "Structure inherits all fields from " + m.BOLT
            #     s += st["parentName"] + m.BOLT + " and add these" + m.BR
            #     parentstr = m.ROW + "Parent" + m.COL + m.genInternalLink(st["parentName"]) + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
            #     #parentstr = m.ROW + "Parent" + m.COL + st["parentName"] + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
            # else: 
            #     parentstr = ""
            #     s += "Fields in this structure" + m.BR
            s += m.ROW + "Tag" + m.COL + "Value" + m.COL + "Comment"  + m.COL
            s += m.ROW + "------" + m.COL + "-----" + m.COL + "------------------------------"  + m.COL
            for vv in enm["values"]:
                if "comment" in vv: cmt = cleanstr(vv["comment"])
                else: cmt = ""
                if "comment2" in vv: cmt += " " +vv["comment2"]
                s += m.ROW + vv["name"] + m.COL + vv["value"] + m.COL + cleanstrNL(cmt) + m.COL
            s += m.NLNL 
        return s        
    def genDocStructs(m):
        s  = m.H2 + "Structures\n" + m.LINE
        for st in structList:
            #s += m.LINE
            s += m.H3 + st["name"] +"\n"
            if "comment" in st:
                s += cleanstr(st["comment"]) +m.NLNL
            if "anno" in st:
                s += m.BR + m.BOLT+ "Annotations" + m.BOLT+ m.NLNL
                for loc in st["anno"]:
                    #s1 = loc.get("value","") + loc.get("eval","") + loc.get("sval","") 
                    s1 = ""
                    s += m.LIST +  loc["name"]  + "  =  " + s1 + m.NLNL
            if "localConst" in st:
                s += m.BR + m.BOLT+ "Structure locals constants" + m.BOLT+ m.NLNL
                for loc in st["localConst"]:
                    s1 = loc.get("value","") + loc.get("eval","") + loc.get("expr","") 
                    s += m.LIST +  loc["name"]  + "  =  " + s1 + m.NLNL
                #if table
                # s += "Structure value definitions " + m.NLNL
                # s += m.ROW + "Symbol" + m.COL + "Value" + m.COL + "Comment"  + m.COL
                # s += m.ROW + "------" + m.COL +"-----" + m.COL + "------------------------------"  + m.COL
                # for loc in st["localConst"]:
                #     s1 = loc.get("value","") + loc.get("eval","") + loc.get("sval","") 
                #     s += m.ROW +  loc["name"]  + m.COL + s1 + m.COL + " " + m.COL
                # s += m.NLNL

            if "parentName" in st:
                s += m.BR + "Structure inherits all fields from " + m.BOLT
                s += st["parentName"] + m.BOLT + " and add these" + m.BR
                parentstr = m.ROW + "Parent" + m.COL + m.genInternalLink(st["parentName"]) + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
                #parentstr = m.ROW + "Parent" + m.COL + st["parentName"] + m.COL + "" + m.COL + "This data prepend this structure"  + m.COL
            else: 
                parentstr = ""
                s += "Fields in this structure" + m.BR
            s += m.ROW + "Field" + m.COL + "Type" + m.COL + "Array" + m.COL + "Comment"  + m.COL
            s += m.ROW + "------" + m.COL + "-----" + m.COL +"-----" + m.COL + "------------------------------"  + m.COL
            s += parentstr
            for f in st["body"]:
                if "comment" in f: cmt = cleanstr(f["comment"])
                else: cmt = ""
                if "comment2" in f: cmt += " " +f["comment2"]
                if "arrLen" in f: 
                    arrLen = f["arrLen"]
                else: 
                    arrLen = "-"
                if f["type"].find("enum")>=0: 
                    etxt  = f["enumName"]
                    vtype = f["type"] + " " + m.genInternalLink(etxt,"enum-"+etxt)
                elif f["type"] in structDict: 
                    etxt  = f["type"]
                    vtype = f["type"] + " " + m.genInternalLink(etxt,etxt)
                else: vtype = f["type"]
                s += m.ROW + f["name"] + m.COL + vtype + m.COL + arrLen + m.COL + cleanstrNL(cmt) + m.COL
            slen,ret = m.genPackLenCalc(st)    
            simlen,canSimplify = m.simplifyEq(slen)
            if canSimplify : simlen = str(simlen) 
            else : simlen = "variable"
            s += m.ROW + "Total" + m.COL + " length" + m.COL + simlen + m.COL + slen  + m.COL
            s += m.NLNL 
        return s

    def genDocHeader(m):
        s = ""
        if "doc_header" in annotateDict:
            s += m.H1 +  cleanstr(annotateDict["doc_header"])+ m.NLNL
        else:
            s += m.H1 +  "Title" + m.NLNL
        s += m.H3 
        if "name" in annotateDict:
            s += cleanstr(annotateDict["name"])
        if "version" in annotateDict:
            s += " version " + cleanstr(annotateDict["version"])
        s +=  m.NLNL
        s += m.LINE
        if "doc_intro" in annotateDict:
            s += m.H2 + "Intoduction\n" + cleanstr(annotateDict["doc_intro"]) + m.NLNL
        return s
    def genAll(m):
        s  = m.genDocHeader()      
        s += m.DLINE
        s += m.genDocEnums()
        s += m.DLINE
        s += m.genDocStructs()
        return s




class OOpythonGenerator(OOcodeGenerator):
    def __init__(self):
        self.typeTable1           = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
        self.codeCommentStart    = "''' "
        self.codeCommentEnd      = " '''"
        self.codeCommentLineStart= "# "
        self.doxPre              = "\n    :"         # pydoc prefix
        self.doxPost             = ":"         # pydoc prefix
        #typeTable2           = {"string":"","zstring":"char","ustring":"wchar","uzstring":"wchar"}
        # set the language
        self.LANG = BaseCodeGenerator.LANG_PY
    def lookupType(self,vartype):  
        return ""
    def genEnumStart(self,enm):
        return  "\nclass "+enm["enumName"] + "(IntEnum):"
    def genEnumEnd(self,enm):
        return  "\n"  
    def genClassDeclBegin(self,structname,parentstruct= None):
        s = "class "+structname
        if parentstruct is not None: 
            s += "(" + parentstruct + ")"
        return s + ":\n"
    def genClassDeclEnd(self,structname):
        return "\n\n"
    def genAll(self,fname):
        s  = "from enum import Enum\n"
        s += annotateDict.get('py_imports',"")
        s += annotateDict.get('py_code',"")
        s += self.genAllEnumDefs(separator = "")
        for st in structList:
            s += self.genClassImplementation( st) +"\n"

        return s





test1 = """
@name       =  "Test BBX"
@version    =  "0.1-4"
@doc_title  =  "BBX document"
@doc_header =  "BBX document heading generation Testing"
@doc_intro  =  '''This is the definiton of the message protocol
                  used for bla-bla-bla'''

@c_includes =  '''
#include <stdio.h>
#include "comms.h"
'''

@c_code = '''
void testfun(void)
{
   dosomething();
} // end test
'''

/* 
 This is the common header for everybody.
*/
struct GGheader
{
    /* This is to test a very long comment line. 
       The destination is where the message should be send to.
       Each device should be allocated a fixed address.
    */
  uint8     dest;   // Alt dest comment
  MSGID16   mM; // This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
  uint16    msg_id = MSG_ID; // This is to test a very long comment line. Abcdefghijklmnopqrstuvwxyz abcdefghijklmnopqrstuvwxyz
  CRC16     CalcCrc16[dest:msgid];  //  CRC16     CalcCrc16(dest..msgid); 
}  

enum Gender {
    UNKNOWN = 0;    
    MALE    = 1;   // set as male
    FEMLE   = 0x2;   // set as female
    OTHER   = 0x3;   // if a person identifies with a different gender 
}

/*
  This is the message to set the user profile.
  Line 2 of comment
*/
struct SetProfile headedby GGheader 
@CC=56
@CV=542
<MSG_ID = 0x1155>  <ARRLEN = 10>
{ 
  int32 id = 1;      // the user identificatin number
  char[20]  surname; // the user surname
  enum8     ename  fieldvarname {  x1=1; x2=2; a1 = 3;  };

  enum8  Gender gender;
  int8     dlen;
  CRC16     hdrCrc2[dest:dlen]; // a message calculated crc
  char[dlen]    addit;
  zstring email = "eeeeee"; 
}"""




GGcomsDef = """
@name       =  "GGCommsDefinition"
@version    =  "1.0-0"
@doc_title  =  "Greatguide Communications Protocol Definition"
@doc_header =  "BXB definition document"
@doc_intro  =  '''This is the definiton of the message protocol
                  used between the seat units and the master streamer'''

@c_includes =  '''
#include <stdio.h>
#include "comms.h"
'''

@c_code = '''
void testfun(void)
{
   dosomething();
} // end test
'''

/* These are the main commands.
*/
enum cmd_t { 
    CMD_BROADCAST      = 0x0A;  // All messages using this tag will be broadcasted to all addresses, e.g. audio files 
    CMD_BROADCAST_ACK  = 0x03;  // An ackowladge if the broadcast command was sucessfull 
    CMD_READ           = 0x15;
    CMD_READ_ACK       = 0x16;
    CMD_WRITE          = 0x29;
    CMD_WRITE_ACK      = 0x30;  // Acknowladge send on a write
    CMD_WR_SLAVE       = 0x3D;  // Not used: Reserved to be used to write to a single seat unit.
    CMD_DEBUG          = 0x1A;  // Debug command only and should be ignored otherwise.
    CMD_NACK           = 0x04;  // A negative ackowladge used if any command failed  
    CMD_ACK_HEADER     = 0x05;  // An ackowladge used if the header was recieved withhout error.  
    }


/* 
 This is the common header for all messages. 
*/
struct MsgHeader
{
    /* This is a magic number that indicates the start of the message */
    uint32  magic = 0x900DBEEF;
    /*
       The destination address is where the message should be send to.
       Devices are allocated a fixed address. The address for the master streamer 
       is always 0. Seat units are each configured with ther own addresses.
       Messages can be either directed to a single device or broadcasted 
       depending on the command. If it is a broadcast command the destination
       will still be for a spesific address and that address should send CMD_BROADCAST_ACK
       acknowladges or a CMD_ACK_HEADER on sucess or a CMD_NACK on an error. 
       When broadcasted the broadcast address 
    */
    uint8       destAddr;   
    uint8       sourceAddr;         // The source address.
    enum8 cmd_t    cmd    = CMD_ID; // This is the message identifier. 
    
}  

/*
  The read command reads information from the seat units, normally statistics 
  and state changes. The seat unit should respond with a CMD_READ_ACK or 
  CMD_NAC on failure.
*/
struct ReadMsg headedby MsgHeader
@CC=56
@CV=542
<CMD_ID = 0x15>  <ARRLEN = 10>
{
      
    enum8 read_t   subCmd ;         // 
    uint16         len    = 0;     // no data send with this message
    /*
      A sequence number assosiated with this message and returned 
      by the CMD_READ_ACK
    */
    uint16         seqNr;       // crc use for integrity checking
    CRC16          crc16[destAddr:seqNr]; 
}

enum Gender {
    UNKNOWN = 0;    
    MALE    = 1;   // set as male
    FEMLE   = 0x2;   // set as female
    OTHER   = 0x3;   // if a person identifies with a different gender 
}

/*
  This is the message to set the user profile.
  Line 2 of comment
*/
struct SetProfile headedby MsgHeader 
@CC=56
@CV=542
<MSG_ID = 0x1155>  <ARRLEN = 10>
{ 
  int32 id = 1;      // the user identificatin number
  char[20]  surname; // the user surname
  enum8     ename  fieldvarname {  x1=1; x2=2; a1 = 3;  };

  enum8  Gender gender;
  int8     dlen;
  CRC16     hdrCrc2[dest:dlen]; // a message calculated crc
  char[dlen]    addit;
  zstring email = "eeeeee"; 
}"""

def mainTest2():
    parseBxbDefStr(GGcomsDef)
    docgen = MarkdownGenerator() 
    s = docgen.genAll()
    print(s)


def mainTest():
    pp = parser.parseString(test1)
    pygen = OOpythonGenerator()
    pygen.pprint()
    s = pygen.genAll()
    print(s)
    print("\n------------------------------\n\n")
    oogen = OOcodeGenerator()
    #oogen.pprint()
    s = oogen.genAll("test.hpp","test.cpp")
    print(s)

if __name__ == "__main__":
    # execute only if run as a script
    mainTest2()