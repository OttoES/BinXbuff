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

def convertCamelToSnake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

def convertSnakeToCamelCase(column):
   first, *rest = column.split('_')
   return first + ''.join(word.capitalize() for word in rest)
    
def parseBxbDefFile(fileName):
    parser.parseFile(fileName)
    # docgen = MarkdownGenerator() 
    # s = docgen.genAll()
    # print(s)


def parseBxbDefStr(defStr):
    parser.parseString(defStr)
    # docgen = MarkdownGenerator() 
    # s = docgen.genAll()
    # print(s)

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
    doxPost             = " "            # doxygen postfix
    typePostfix         = "_t"
    #funcNamePrefix      = "BIN_"
    funcPackCallPrefix  = "BIN_call"
    funcPackBaseName    = "pack"
    funcUnpackBaseName  = "unpack"
    funcPackInBuff      = "packIntoBuffer"
    funcUnpackInStruct  = "unpackIntoStruct"
    #funcCopyStruct      = "copyStruct"
    funcCreateName      = "objFactory"
    funcCreateFromBufName= "objFactory"
    funcProcessBuffName = "CallStoreSendBuffer"
    funcUnpackNamePrefix= "BIN_unpack"
    funcProcessFunPrefix= "BIN_process"              # prefix for the functions that process incoming messages
    noTypeName          = "void" 
    intTypeName         = "int"
    bufTypeName         = "uint8_t"
    lenTypeName         = "size_t"                  # buffere length etc
    singletonFuncDecl   = "\n// singleton function\n"# will be static if in a class
    privateFuncDecl     = "static "                  # will be private if in a class
    errorHandlerName    = "printf"                   # function that will be called on an error  
    constErrBuffOutOfBounds = "ERR_BUFF_OUT_OF_BOUNDS"
    constErrBuffShort   = "ERR_BUFF_OUT_OF_DATA"
    constErrUnknownTag  = "ERR_TAG_UNKNOWN"
    constErrCRC         = "ERR_CRC_FAIL"
    constErrNotEqual    = "ERR_VALUE_NOT_EQUAL"
    typeTable1          = {"bool":"bool","char":"char","int":"int"}
    typeTable2          = {"string":"char","zstring":"char","ustring":"wchar","uzstring":"wchar"}
    # these types are internally generated and not passed in by the user  
    typeTableLoc        = {"CRC8":"uint8","CRC16":"uint16","CRC32":"uint32","MSG_ID16":"uint16"}
    typeTableEnum       = {"enum8":"int8","enum16":"int16","enum32":"int32"}
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
    #TODO: can it be removed?
    def lookupType(self,vartype):  
        if vartype in self.typeTable2: return  self.typeTable2[vartype]
        if vartype in self.typeTable1: return  self.typeTable1[vartype]
        return vartype+self.typePostfix          
    def lookupFieldType(self,fieldd):
        vartype = fieldd["type"]
        if vartype.startswith("enum"):
            return "enum "+fieldd["enumName"]
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
        #varType = self.lookupType(varType)
        return "const " + varType + " "+varName  + " = (const "+varType+") ("+varVal+  ");"
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
    # TODO: stillused??
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
    # def genPackVar(self,buff,buffpos,vartype,varname, varval): 
    #     #if vartype in self.typeTable2: 
    #     #    return self.funcPackNamePrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
    #     return self.funcPackCallPrefix+vartype+"("+buff+", "+buffpos+", "+varname+","+varval+");"
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
    def makeFuncDeclr(self,structt,retType,funName,args,isSingletonFun = False,isPrivate = False):
        """ Make a valid function declaration

        Arg:
          funName    - the base name (root) of the name. If it is part of a class
                       it should be prefixed wih the class name (or what ever the 
                       programming language require)
          args       - function arguments
          isSingletonFun  specifies whether it is a static class member 
          isPrivate       means that it will not be called externally
        """
        s = ""
        if isPrivate:      s+= self.privateFuncDecl
        if isSingletonFun: s+= self.singletonFuncDecl
        #nn = structt['name'].upper() + "_" + funName
        nn = convertCamelToSnake(structt['name']) + "_" + funName
        s += retType + " " + nn + "(" + args + ")"
        return s
    def makeDeclFunArgList(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = "," , inclParent = True , inclConst = False, inclPrivate = False )    
    def makeCallFunArgList(self,structt):
        return self.makeFieldListGeneric(structt,False, seperator = "," , inclParent = True , inclConst = False, inclPrivate = False )
    def makeDeclFunArgListAll(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = "," , inclParent = True , inclConst = True, setInitValue = False )
    def makeCallFunArgListAll(self,structt):
        return self.makeFieldListGeneric(structt,False, seperator = "," , inclParent = True , inclConst = True )
    def makeClassMemberList(self,structt):
        return self.makeFieldListGeneric(structt,True, seperator = ";\n  " , inclParent = False , inclConst = True )
    def makeFieldListGeneric(self,structt,inclTypes, seperator = "," , inclParent = True , inclConst = False, noLastSeparater = True, inclArrLen =False, inclPrivate = False,setInitValue = True ):
        """ Flexible generation of variable/argument list 
        """
        fields    = structt["body"]
        s = ""
        if inclParent and "parentName" in structt:
            parnt = self.getParent(structt)
            s += self.makeFieldListGeneric(parnt,inclTypes, seperator, inclParent , inclConst,inclArrLen = inclArrLen,setInitValue =setInitValue) + seperator
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
                s += self.genVarDecl(f, inclArrLen = inclArrLen, termstr = seperator,setInitValue = setInitValue ) 
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
        return str(ll),True
    def genVarDecl(self,sfield,inclArrLen =False, termstr = ";", setInitValue = True):
        if not "type" in sfield:
            return "" 
        vtype = sfield["type"]
        vname = sfield["name"]
        if vtype in self.typeTableEnum: 
            s = "enum "+ sfield["enumName"] +" "+vname
        elif vtype in self.typeTable2: 
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
    # def oldisFuncRequired(self,structt,funct,lang):
    #     """Check if this function should be generated.

    #        More or less the following logic:
    #           - look at struct annottion
    #           - look at global language anotation
    #           - look at global annottion
    #     """
    #     # local annoation takes precedence so first look at that
    #     if "anno" in structt:
    #         lst     = structt["anno"]
    #         anno = self.findInConstList(lst,lang+"_"+funct)
    #         if anno: return True
    #         anno = self.findInConstList(lst,lang+"_"+funct+"_FALSE")
    #         if anno: return False
    #         anno = self.findInConstList(lst,funct)
    #         if anno: return True
    #         anno = self.findInConstList(lst,funct+"_FALSE")
    #         if anno: return False
    #     lst     = annotateDict
    #     if lang+"_"+funct in lst:
    #         return True
    #     if lang+"_"+funct+"_FALSE" in lst:
    #         return False
    #     if funct in lst:
    #         return True
    #     if funct+"_FALSE" in lst:
    #         return False
    #     return True

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
    def genPackFieldCode(self,f,deref = ""):
        # if deref is None:
        #     preamble = self.lookupFieldType(f)+"  "
        # else:
        #     preamble = deref
        tsize = self.lookupTypeSize(f["type"])
        if "arrLen" in f:  
            # if it is a structure array unpack in a loop
            if f["type"] in structDict:
                s  = "int ii;\n"
                #s += self.lookupFieldType(f) + "  " + f["name"] +"[" + f["arrLen"] + "];\n"
                s += "for (ii = 0; ii < "+ f["arrLen"] +" ;ii++) {\n"
                args = "&"+f["name"]+"[ii],&buff[pos],bufSize-pos"
                #s += "  int ret = "+f["type"]+self.funcPackInBuff+"("+f["name"]+"[ii],&buff[pos],bufSize-pos);\n"
                if f["type"] in structDict:
                    s += "  int ret = "+self.makePackInStructDecl(structDict[f["type"]],args) +";\n"
                s += "  if (ret < 0) return ret;\n"
                s += "  pos += ret;\n"
                s += "} // for ii\n"
                return s
            lenstr = str(tsize)+"*" + f["arrLen"]
            # TODO: Maybe would be beer have a makeArrayDecl
            s = "// just copy but no valid if endianess differ\n" 
            #self.lookupFieldType(f) + "  " + f["name"] +"[" + f["arrLen"] + "];\n"
            ## this is only valid if the endianess is the same for multibyte types !!!!
            s += "    memcpy("+self.packBuffName+"+pos,"+f["name"] +","+lenstr + ");\n"
            s += "    pos += "+ lenstr + ";\n"
            return s
        if tsize == 1:
            return self.packBuffName+"[pos++] = (uint8_t)"+deref+ f["name"] + ";\n"
            #return self.packBuffName+"[pos++] = (uint8_t)"+ f["name"] + ";\n"
        elif tsize == 2: 
            # this is stored in little endian
            s = self.packBuffName+"[pos++] = (uint8_t)"+deref+ f["name"] + ";\n"
            return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+deref+ f["name"] + ">>8);\n"
        elif tsize == 4: 
            # this is stored in little endian
            s  = self.makeLineComment(" it is faster to copy byte by byte than calling memcpy()")
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)"+deref+ f["name"] + ";\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+deref+ f["name"] + ">>8);\n"
            s += "    "+ self.packBuffName+"[pos++] = (uint8_t)("+deref+ f["name"] + ">>16);\n"
            return s + "    "+ self.packBuffName+"[pos++] = (uint8_t)("+deref+ f["name"] + ">>24);\n"
        s  = "pos    += " + self.funcPackCallPrefix + f["type"].capitalize() 
        s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s
    def genUnpackFieldCode(self,f,deref = None):
        """
        Generate code to unpack the the data from the byte array into
        a variable

        f       is the field
        deref   indicaae if the variabe should  be dereferenced like in the case oof a class
        """
        if f['type'] == "enum8":
            print ("ffffffffg")
        if deref is None:
            preamble = self.lookupFieldType(f)+"  "
        else:
            preamble = deref
        tsize   = self.lookupTypeSize(f["type"])
        bufname = self.packBuffName 
        if "arrLen" in f:  
            # if it is a structure array unpack in a loop
            if f["type"] in structDict:
                s  = "int ii;\n"
                s += self.lookupFieldType(f) + "  " + f["name"] +"[" + f["arrLen"] + "];\n"
                s += "for (ii = 0; ii < "+ f["arrLen"] +" ;ii++) {\n"
                #s += "  int ret = "+f["type"]+self.funcUnpackInStruct+"("+f["name"]+"[ii],&buff[pos],buflen-pos);\n"
                s += "  int ret = "+convertCamelToSnake( f["type"])+"_"+self.funcUnpackBaseName+"(&"+f["name"]+"[ii],&buff[pos],buflen-pos);\n"
                s += "  if (ret < 0) return ret;\n"
                s += "  pos += ret;\n"
                s += "} // for ii\n"
                return s
            # normally an array od a base type 
            #  - else unknown type and will give a compile error
            lenstr = str(tsize)+"*" + f["arrLen"]
            # type declaration
            # TODO: Maybe would be beer have a makeArrayDecl
            s = self.lookupFieldType(f) + "  " + f["name"] +"[" + f["arrLen"] + "];\n"
            # TODO: this is only valid if the endianess is the same for multibyte types !!!!
            return s + "memcpy("+f["name"] +","+bufname+"+pos,"+lenstr + ");\n"
        if tsize == 1:
            return  preamble+ f["name"] + " = ("+self.lookupFieldType(f)+ ")" + bufname+"[pos++] " + ";\n"
        elif tsize == 2: 
            # this is  little endian
            return  preamble +f["name"] + " = ("+ self.lookupFieldType(f)+ ")(" + bufname+"[pos] + ("  + bufname+"[pos+1]<<8)" +  ");\npos +=2;\n"
            #return  self.lookupType(f["type"])+"  "+f["name"] + " = ("+ self.lookupType(f["type"])+ ")(" + bufname+"[pos] + ("  + bufname+"[pos+1]<<8)" +  ");\npos +=2;\n"
        elif tsize == 4: 
            # this is  little endian
            return  preamble +f["name"] + " = ("+ self.lookupFieldType(f)+ ")(" + bufname+"[pos] + ("  + bufname+"[pos+1]<<8) + (((uint32_t)"+ bufname+"[pos+2])<<16) + (((uint32_t)"+ bufname+"[pos+3])<<24)) " +  ";\npos +=4;\n"
            #return  self.lookupType(f["type"])+"  "+f["name"] + " = ("+ self.lookupType(f["type"])+ ")(" + bufname+"[pos] + ("  + bufname+"[pos+1]<<8) + (((uint32_t)"+ bufname+"[pos+2])<<16) + (((uint32_t)"+ bufname+"[pos+3])<<24)) " +  ";\npos +=4;\n"
        # if we get here it is probably a single struct
        s  = f["type"] + self.typePostfix + "  " + f["name"] + ";\n"

        if f["type"] in structDict: 
            s += "// Read a structured type\n"
            structt = structDict[f["type"]]
            args    = "&"+f["name"] +",buff,pos"
            tmpvar  = f["name"]+"_ret"
            s += self.intTypeName +" " +tmpvar + " = " + self.makeUnpackFunCall(structt,args,namePrefix = "") + ";\n"
            s += "if (" +tmpvar+" <0) return "+tmpvar+";\n" 
            s += "pos += " + tmpvar +";\n"
        else:
            s += "// Unknown type found - generate a skeleton \n"
            s += "pos    += " + self.makeFuncDeclr(f,"",self.funcUnpackInStruct,"???") +";\n"

        #s += "pos    += " + self.funcPackCallPrefix + f["type"].capitalize() 
        #s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s
    def genPackFields(self,structt,structPrefix = ""):    
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
                s += "    " + self.makeConsVarDecl(self.lookupFieldType(f) ,f["name"],f["value"]) +"\n"
                #s += "    " + self.makeConsVarDecl(f["type"],f["name"],f["value"]) +"\n"
            if "callName" in f :
                #if "annoCheckVal" in f:   # should the constant value be checked
                    #s1 += self.makeLineComment(" call function to calc value")
                    arg1 = self.replaceSymbsInFieldAssgn(structt,f["arg1"]); 
                    arg2 = self.replaceSymbsInFieldAssgn(structt,f["arg2"]); 
                    s += "    "+ self.makeLineComment("call user function with "+f["arg1"]+" and " +f["arg2"])
                    funCallStr = f["callName"]+"(" +self.packBuffName +","+arg1+","+arg2 +")"
                    s += "    "+self.makeConsVarDecl(self.lookupFieldType(f),f["name"],funCallStr) +"\n"
            s += "    " + self.genPackFieldCode(f,deref=structPrefix) 
            #s += "    pos    += " + self.funcPackNamePrefix + f["type"].capitalize() 
            #s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        return s 
    def replaceSymbsInFieldAssgn(self,structt,expr):
        # TODO: add more stuff such as expressions with keywords
        if expr[0] == "&":  # needs buffpos/address of the field
            s1,pres = self.genPackFieldPosCalc(structt,expr[1:],includeField=False)    
            if pres: return s1
        if expr[-1] == "&":  # needs position in buff including this field
            s1,pres = self.genPackFieldPosCalc(structt,expr[:-1],includeField=True)    
            if pres:
                s1,__  = self.simplifyEq(s1)
                return s1
        return expr

    def genUnpackFields(self,structt):
        if self.isStructDeclUsed(structt):
            stuctderef = "this->"    
        else:
            stuctderef = None
        fields    = structt["body"]
        s = ""
        s1  = "    "
        for f in fields:
            # TODO: this will probably be remove - replace with @ function call 
            if f["type"] == "CRC16":
                p1,fnd1 = self.genPackFieldPosCalc(structt,f['rangeStart'],False)
                p2,fnd2 = self.genPackFieldPosCalc(structt,f['rangeEnd'],True)
                s += "    ??int16_t   "+f["name"] +" += CalcCRC16"+f["name"]+"("+self.packBuffName+", "+p1 + "," + p2 + ");\n" 
            s1 += self.genUnpackFieldCode(f,deref = stuctderef) 
            # s1 += "// "+ f["type"] + " -> " + self.lookupFieldType(f) +    "\n"
            # check if it is assigned a value
            if "value" in f :
                if "annoCheckVal" in f:   # should the constant value be checked
                    s1 += self.makeLineComment(" check the field value is equal to the expected value")
                    #s1 += self.makeConsVarDecl(f["type"],"_"+f["name"],f["value"]) +"\n"
                    s1 += "if ("+f["name"] +" != "+f["value"] +") return "+self.constErrNotEqual+ ";" +"\n"
                else:
                    s1 += self.makeLineComment(" this is an assigned value but not verified here")
                    #s1 += self.makeConsVarDecl(f["type"],f["name"],f["value"]) +"\n"
            # the field is assigned to a functions call
            if "callName" in f :
                if "annoCheckVal" in f:   # should the constant value be checked
                    s1 += self.makeLineComment(" check the field value is equal to the returned function value")
                    arg1 = self.replaceSymbsInFieldAssgn(structt,f["arg1"]); 
                    arg2 = self.replaceSymbsInFieldAssgn(structt,f["arg2"]); 
                    s1 += self.makeLineComment("call user function with "+f["arg1"]+" and " +f["arg2"])
                    funCallStr = f["callName"]+"(" +self.packBuffName +","+arg1+","+arg2 +")"
                    #s1 += self.lookupType(varType) + " " + "ret_"+f["name"] + " = " + 
                    s1 += self.makeConsVarDecl(self.lookupFieldType(f),"ret_"+f["name"],funCallStr) +"\n"
                    s1 += "if ("+ "ret_"+f["name"] +" != "+f["name"] +") return "+self.constErrNotEqual+ ";" +"\n"
            #s += "(" +self.packBuffName +", pos,"+ f["name"] + ");\n"
        # fixup the indentation
        s += s1.replace("\n","\n    ")
        # # call the user function
        # funname = self.getLocalAnno(structt,"call_after_unpack",default = "userfun")
        # funname = cleanstr(funname)
        # s += funname + "(" +self.packBuffName +", pos);\n"
        return s 
    # includeField inidcate if the field named fieldName should be included in the position calculations    
    def genPackFieldPosCalc(self,structt,fieldName,includeField):    
        fields    = structt["body"]
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
        s     = self.makeFuncDeclr(structt,structt['name'],namePrefix+self.funcCreateName,args)
        return s
    def genCreateFromBuffFunDecl(self,structt,copyToBuff=True,msgIdArg = False,namePrefix = ""):
        args  = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" len "
        s     = self.makeFuncDeclr(structt,structt['name'],namePrefix+self.funcCreateFromBufName,args)
        return s
    def makeUnpackFunCall(self,structt,args,namePrefix = ""):
        return self.makeFuncDeclr(structt,"",namePrefix+self.funcUnpackBaseName,args)
    def genUnpackFunDecl(self,structt,copyToBuff=True,classLike=False,namePrefix = ""):
        s  = "\n"
        # generate the comments
        s += self.codeCommentStart
        s += self.doxPre + "param buff[]    buffer with data to be unpacked "
        s += self.doxPre + "param buflen    number of bytes in buff, must be at long enough for complete struct "
        s += self.doxPre + "return if > 0 : position in array of last extracted data"
        s += self.doxPre + "return if < 0 : error in data stream (-4: too short, -23: CRC error"
        s += "\n" + self.codeCommentEnd +"\n"
        args  = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" buflen "
        #if classLike:
        if self.isStructDeclUsed(structt):
            args = structt["name"]+self.typePostfix +"* this,"+args
        s += self.makeFuncDeclr(structt,self.intTypeName,namePrefix+self.funcUnpackBaseName,args)
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
            args = "uint8_t  "+self.packBuffName+"[],"+self.intTypeName +" bufSize, "
        else: args = ""
        args += self.makeDeclFunArgList(structt)
        #-- build the function call
        s += self.makeFuncDeclr(structt,self.intTypeName,namePrefix+self.funcPackBaseName,args)
        return s
    def genPackFieldAssignments(self,structt,structPrefix = ""):
        s = ""
        if "parentName" in structt:
            # fill in the inherited data from the parent
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            s += self.genPackFieldAssignments(parentStruct,structPrefix=structPrefix)
        # build the assignment of the data fields to the buffer
        s += self.genPackFields(structt,structPrefix = structPrefix )
        return s
    def genPackFun(self,structt,msgIdArg = False,namePrefix = ""):
        # determine if the function should be defined 
        ret = self.getLocalAnno(structt,"pack","TRUE")
        if ret == "FALSE" : return ""    # function should not be generated
        # determine if a function call in pack is defined
        callFuncName          = self.getLocalAnno(structt,"call_in_pack","FALSE")
        localBuffAndUserFunct = (callFuncName != "FALSE")
        #parentArgs            = ""
        s  = self.genPackFunDecl(structt,copyToBuff= not localBuffAndUserFunct,msgIdArg = msgIdArg,namePrefix = namePrefix)
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
        s += ";\n"
        s += "          "+self.intTypeName +" pos    = 0;\n"
        if localBuffAndUserFunct:
            s += "    uint8_t   "+self.packBuffName+"["+self.packBuffName+"Len];\n"
        else:
            s += "    if ("+self.packBuffName+"Len > bufSize) return "+self.constErrBuffShort+";   "+self.makeLineComment("buffer to small")
        if "parentName" in structt:
            # fill in the inherited data from the parent
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            s += self.genPackFields(parentStruct)
        #-- build the assignment of the data fields to the buffer
        s += self.genPackFields(structt)
        # if a funcion must be called before return 
        if localBuffAndUserFunct:
            s += "    return  "+callFuncName+"("+self.packBuffName
            s += ", pos);\n"
        else:
            s += "    return  pos;\n"
        s += "\n} // end\n"
        return s

    #     def makeUserAferUnpackFunDecl(self,structt):
    def makeUserAferUnpackFunDecl(self,structt,inctypedecl=False): #,callParentUnpack=False,classLike=False,namePrefix = ""):
        if not self.isStructDeclUsed(structt):
            defaultfunname = convertCamelToSnake(structt['name']) + "_" +"userfun"
            funname = self.getLocalAnno(structt,"call_after_unpack",default = defaultfunname)
            funname = cleanstr(funname)
            if inctypedecl:
                args    = self.bufTypeName + " "+ self.packBuffName+"[]," +self.intTypeName + " pos"+"," + self.makeDeclFunArgList(structt)
                return self.intTypeName +" " + funname + "(" +args+");\n"
            else:
                args    = self.packBuffName +", pos," + self.makeCallFunArgList(structt)
                return "    "+funname + "(" +args+");\n"
        return ""
    def makePackInStructDecl(self,structt,args = None,inctypedecl=False): #,callParentUnpack=False,classLike=False,namePrefix = ""):
        if self.isStructDeclUsed(structt):
            funname = convertCamelToSnake(structt['name']) + "_" + self.funcPackInBuff # funcCopyStruct
            if args is None:
                args  = structt["name"]+self.typePostfix +"* this, uint8_t buff[],int bufLen"
                return self.intTypeName + " " +funname+ "("+args+")\n"
            else:
                return " " +funname+ "("+args+")"
        return ""
    def genUnpackFun(self,structt,callParentUnpack=False,classLike=False,namePrefix = ""):
        # determine if the function should be defined 
        ret = self.getLocalAnno(structt,"unpack","TRUE")
        if ret == "FALSE" : return ""    # function should not be generated
        s  = self.genUnpackFunDecl(structt,classLike=False,namePrefix = namePrefix)
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
                s += "    pos += "+self.makeFuncDeclr(structt,"",funname,args = "buff,pos") + ";\n"
            else:
                #s += "    if ("+self.packBuffName+"Len > bufSize) return 0;   // buffer to small\n"
                s += self.genUnpackFields(parentStruct)

        #-- build the assignment of the data fields to the buffer
        s += self.genUnpackFields(structt)
        # make sure that the buffer had enough data
        s += "if ( pos > buflen) return "+ self.constErrBuffShort +";\n"
        # call the user function only if not implemented as struct
        if not self.isStructDeclUsed(structt):
            s += self.makeUserAferUnpackFunDecl(structt)
            # defaultfunname = convertCamelToSnake(structt['name']) + "_" +"userfun"
            # funname = self.getLocalAnno(structt,"call_after_unpack",default = defaultfunname)
            # funname = cleanstr(funname)
            # args    = "," + self.makeCallFunArgList(structt)
            # s      += "    "+funname + "(" +self.packBuffName +", pos"+args+");\n"
        s += "    return  pos;\n"
        s += "} // end\n"
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
    def makeUserProcessMsgDecl(self,structt):
        s  = "void "+ self.funcProcessFunPrefix + structt["name"] +"("
        s += self.makeDeclFunArgListAll(structt)
        s += ");\n"
        return s

    def genProcessMsgDetail(self,structt):
        s  = "      "+self.makeLineComment( "unpack each field into a variable")
        #s += self.genVarDecl(sfield,inclArrLen =False, termstr = ";")
        #s += "      " + self.makeFieldListGeneric(structt,inclTypes = True, seperator = ";\n      " , inclParent = False , inclConst = False,  noLastSeparater = False ,inclArrLen =True )
        s1 = "      "
        for f in  structt["body"]:
           s1 += self.genUnpackFieldCode(f) 
        s  += s1.replace("\n","\n      ")
        s += "if (pos > len) "
        s += "   {\n        // error\n        "+self.errorHandlerName+'("Message '+structt['name']+' to short");\n'
        s += '        return '+ self.constErrBuffShort +';\n      }\n'
        s += "      "+ self.makeLineComment("call the (external user) defined function with the unpacked data")
        s += "      "+ self.funcProcessFunPrefix + structt["name"] +"("
        s += self.makeCallFunArgListAll(structt)
        s += ");\n"
        return s

    # TODO: still used??
    # def genProcessMsgFuns(self):
    #     #find the base messages
    #     s = ""
    #     for st in structList:
    #         if "localConst" in st:
    #             lst     = st["localConst"]
    #             bstruct = self.findInConstList(lst,"MSG_BASE")
    #             # if MSG_BASE is declared, a message select and unpack is created
    #             if bstruct :
    #                 s += self.genSelecAndProcessMsgFun(st)            
    #     return s

    def genSelecAndProcessMsgFun(self,baseStructt):
        s  = "\n// This is the base message parser that should be called with\n// the byte array to be translated to a spesific message\n"
        s += "// First determine the struct/message type based on MSG_ID and\n// MSG_COND and then unpack\n"

 
        s += self.genUnpackFunDecl(baseStructt,namePrefix = "tmpPrefix")
        s += "\n{\n"
        s += "    "+self.intTypeName +" pos = 0;\n"
        if "parentName" in baseStructt:
            s += "\nERROR: base or header should not have a parent\n"

        # build the assignment of the data fields to the buffer
        s += self.genUnpackFields(baseStructt)

        # s += "\n}\n -- old \n"
 
        # # old code

        # #s += self.singletonFuncDecl + self.lenTypeName + " " + "parseMsg(uint8_t buff[],int len) \n{\n"
        # s += self.makeFuncDeclr(baseStructt,self.intTypeName,self.funcUnpackNamePrefix, "uint8_t buff[],int len",isSingletonFun=True) + "\n{\n"
        # #s += self.genVarDecl(sfield,inclArrLen =False, termstr = ";")
        # s += "   " + self.makeFieldListGeneric(baseStructt,inclTypes = True, seperator = ";\n   " , inclParent = False , inclConst = False,  noLastSeparater = False ,inclArrLen =True)
        # s1 = ""
        # for f in  baseStructt["body"]:
        #    s1 += self.genUnpackFieldCode(f)
        # s  += s1.replace("\n","\n   ")
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
                    s3 = "    if ("+s1+" && "+s2+") {\n"
                else: 
                    s3 = "    if "+s1+s2+" {    // "+ st["name"] + "\n"
                if len(s1)>1 or len(s2)>1:
                    s += s3+ self.genProcessMsgDetail(st)
                    s += "    } else \n"
            #s += self.genPackFun( st) +"\n"
        s += "    {\n      // error\n      "
        s += self.errorHandlerName+'("Unknown message tag");\n      return '
        s += self.constErrUnknownTag +';\n    }\n'
        s += "    return pos;\n"
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
        s += self.makeConstDecl(self.constErrNotEqual,"-41")
        return s + "\n"

    def genStructFieldDecls(self,structt):
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
    #TODO: remove?
    # def genClasses(self):
    #     s  = ""
    #     for st in structList:
    #       #if self.isStructDeclUsed(st):
    #         s += self.genStructDeclBegin(st['name'])
    #         s += self.genStructFieldDecls(st)
    #         s += self.genStructDeclEnd(st['name'])
    #     return s
    def genCstructIfUsed(self,st):
        s  = "\n"
        if self.isStructDeclUsed(st):
            s += self.genStructDeclBegin(st['name'])
            s += self.genStructFieldDecls(st)
            s += self.genStructDeclEnd(st['name'])
        return s


    def genStructPrototypes(self):
        s  = ""
        for structt in structList:
            # normally C struct are not declared but there are circumstances where it is needed
            s += self.genCstructIfUsed(structt)
            # TODO: cleanup this?
            nn = "" #convertCamelToSnake(structt["name"])
            # if self.isStructDeclUsed(structt):
            #     s += self.genUnpackFunDecl(structt,classLike=True)
            # else:    
            s += self.genUnpackFunDecl(structt,namePrefix = nn ) #,msgIdArg = msgIdArg,namePrefix = namePrefix)
            s += ";\n"
            s += self.genPackFunDecl(structt,namePrefix = nn)
            s += ";\n"
            # special additonal struct copy function
            if self.isStructDeclUsed(structt):
                s += "static inline "+self.makePackInStructDecl(structt,inctypedecl=True)
                s += "// only for same indianness\n"
                #s += self.intTypeName + " " +structt["name"]+ "_copy(struct "+structt["name"]+ "*ptr,uint8_t buff[],int pos)\n"
                siz,res = self.genPackLenCalc(structt)
                siz,res = self.simplifyEq(siz)
                #s += "{ memcpy(buff,this,"+siz+"); return "+siz+"; }\n"
                s += "{\n    int pos = 0;\n"
                s += self.genPackFieldAssignments(structt,structPrefix = "this->")
                s += "    return "+siz+"; \n}\n"

            # in most cases there is one structure that defines the header
            # this is a special struct that needs more code to full fill its role 
            # as base from which the other messages are 'created'
            if self.isAnnoTagDefined(structt,"MSG_BASE"):
                s += "\n//============== base =================\n\n"
        return s
    # def makeUserAferUnpackFunDecls(self)
    #     s = ""
    #     for structt in structList:
    #         s += self.makeUserAferUnpackFunDecl(structt)
    #     return s   

    def genUserFuncDecls(self):
        s  = ""
        for structt in structList:
            # normally C struct are not declared but there are circumstances where it is needed
            #s += self.genCstructIfUsed(structt)
            s += self.makeUserAferUnpackFunDecl(structt, True)
            if self.isStructDeclUsed(structt):
                s += self.genUnpackFunDecl(structt,copyToBuff=True,classLike=False,namePrefix = "") + ";\n"

                #args = structt["name"]+self.typePostfix +"* this,"+args
                #s += self.makeFuncDeclr(structt,self.intTypeName,namePrefix+self.funcUnpackBaseName,args)
            s += self.makeUserProcessMsgDecl(structt)
        return s

    def genAll(self,hfilename,cfilename= None,userfile=None):
        #pp = hfilename.rfind(".h")
        basename = hfilename.replace(".h","")
        #if pp > 1: basename = basename[:pp]
        if cfilename == None: cfilename = basename + ".c"
        if userfile == None: userfile = basename + "_user.h"
        # generate the prototypes for the functions that must be defined/suplied by  the user
        su  = ""
        su += self.genFileHeader(userfile)
        su += self.makeLineComment("User implemented function declarations")
        su += self.makeLineComment("These functions are called by the generated code")
        su += self.makeLineComment("but must be implemented by the user")
        su += self.makeLineComment("Note that some might not be needed")
        hprot = "__"+userfile.upper().replace(".","_").replace("/","_") +"__"
        su += "#ifndef "+hprot +"\n"
        su += "#define "+hprot +"\n"
        su += '#include "'+hfilename +'"\n'
        su += '#include "inttypes.h"\n'
        su += self.genUserFuncDecls()
        su += "#endif  // "+hprot +"\n"
        # generate header    
        sh  = ""
        sh += self.genFileHeader(hfilename)
        hprot = "__"+hfilename.upper().replace(".","_").replace("/","_") +"__"
        sh += "#ifndef "+hprot +"\n"
        sh += "#define "+hprot +"\n"
        sh += annotateDict.get('c_includes',"")
        sh += '#include "inttypes.h"\n'
        sh += self.genAuxDef()
        sh += self.makeLineCommentDivider()
        sh += self.genAllEnumDefs()
        # TODO: remove???? - now done as part of structure declarations
        #sh += self.genCstructs()
        sh += self.makeLineCommentDivider()
        sh += self.makeLineComment("Function declarations")
        sh += self.makeLineCommentDivider()
        sh += self.genStructPrototypes()
        sh += "#endif  // "+hprot +"\n"
        
        sc  = "// C code \n"
        sc += self.genFileHeader(cfilename)
        sc += '#include "'+hfilename +'"\n'
        sc += '#include "'+userfile +'"\n'
        sc += '#include "string.h"\n'
        sc += annotateDict.get('c_includes',"")
        sc += annotateDict.get('c_code',"")
        for structt in structList:
            sc += self.genPackFun( structt) +"\n"
            sc += self.genUnpackFun( structt) +"\n"
            if self.isAnnoTagDefined(structt,"MSG_BASE"):
                sc += "\n//============== base =================\n\n"
                sc += self.genSelecAndProcessMsgFun(structt)  

        #sc += self.genProcessMsgFuns()
        return sh,sc,su


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
        s += self.genStructFieldDecls(struct)
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
    def genAll(self,hFileName,cFileName):
        # generate h file -------
        s  = self.genFileHeader(hFileName)
        s += "\n"
        s += '#include "inttypes.h"\n'
        #s += annotateDict.get('copyrigh',"")
        s += annotateDict.get('h_includes',"")
        s += self.genAllEnumDefs()
        s += self.genAuxDef()
        for st in structList:
            s += self.genClassDef( st) +"\n"

        # generate cpp file -------
        ss  = self.genFileHeader(cFileName)
        ss += "\n"
        ss += '#include "' + hFileName + "\n"
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
            if canSimplify : simlen = simlen 
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