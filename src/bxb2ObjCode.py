from genBase import *

class OOcodeGenerator(CcodeGenerator):
    typeTable1      = {"bool":"bool","enum8":"uint8_t","char":"char","string":"String"}
    staticFunDecl   = "static "                  # will be private if in a class

    def __init__(self):
        # set the language
        self.LANG = BaseCodeGenerator.LANG_CPP
    def isStructDeclUsed(self,structt):
        return False        
#    def makeAssignByteToArr(self,byteArrName,arrIndx,byteVal):
#        return byteArrName + "[" + arrIndx +"] = (uint8_t)(this."+byteVal+");\n"
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
        #nn = convertCamelToSnake(structt['name']) + "_" + funName
        nn = funName
        s += retType + " " + nn + "(" + args + ")"
        return s

    def genUnpackFun(self,structt,callParentUnpack=True,classLike=False,namePrefix = ""):
        # determine if the function should be defined 
        ret = self.getLocalAnno(structt,"unpack","TRUE")
        if ret == "FALSE" : return ""    # function should not be generated
        s  = self.genUnpackFunDecl(structt,classLike=False,namePrefix = namePrefix)
        s += "\n{ \n"
        s += "    "+self.intTypeName +" "+self.buffPosName+" = 0;\n"
        if "parentName" in structt:
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            if callParentUnpack:
                funname = prn+"::"+self.funcUnpackBaseName
                # s += "    "+self.buffPosName+" += "+self.makeFuncDeclr(structt,"",funname,args = "buff,buflen-"+self.buffPosName+"") + ";\n"
                s += "    "+self.buffPosName+" += "+self.makeFuncDeclr(structt,"",funname,args = "buff,buflen")+";\n"
            else:
                s += self.genUnpackFields(parentStruct)

        # build the assignment of the data fields from the buffer
        s += self.genUnpackFields(structt,stuctderef="")
        # make sure that the buffer had enough data
        s += "if ( "+self.buffPosName+" > buflen) return "+ self.constErrBuffShort +";\n"
        # call the user function only if not implemented as struct
        #if not self.isStructDeclUsed(structt):
        #    s += self.makeUserAferUnpackFunDecl(structt)
        s += "    return  "+self.buffPosName+";\n"
        s += "} // end\n"
        return s
    def genPackFun2(self,structt,msgIdArg = False,namePrefix = ""):
        # determine if the function should be defined 
        ret = self.getLocalAnno(structt,"pack","TRUE")
        if ret == "FALSE" : return ""    # function should not be generated
        # determine if a function call in pack is defined
        callFuncName          = self.getLocalAnno(structt,"call_in_pack","FALSE")
        localBuffAndUserFunct = (callFuncName != "FALSE")
        #parentArgs            = ""
        #s  = self.genPackFunDecl(structt,copyToBuff= not localBuffAndUserFunct,msgIdArg = msgIdArg,namePrefix = namePrefix)
        s  = self.genPackFunDecl(structt,copyToBuff= True,msgIdArg = msgIdArg,namePrefix = namePrefix)
        s += "\n{\n"
        #-- generate constant declaraions for the struct local constant assignments
        locConst = structt.get("localConst",[])    
        for itm in locConst:
            valexp = itm.get("value","")+itm.get("expr","")
            s1 = self.makeConsVarDecl(self.intTypeName,itm["name"],valexp)
            s +=  "    "+ (s1) +"\n"
        #-- calculate the length of the data
        (structLen,__) = self.genPackLenCalc(structt)
        s += "    const "+self.intTypeName +" "+self.buffArrName+"Len = " + structLen
        s += ";\n"
        s += "          "+self.intTypeName +" "+self.buffPosName+"    = 0;\n"
        ##if localBuffAndUserFunct:
        ##    s += "    uint8_t   "+self.buffArrName+"["+self.buffArrName+"Len];\n"
        ##else:
        ##    s += "    if ("+self.buffArrName+"Len > bufSize) return "+self.constErrBuffShort+";   "+self.makeLineComment("buffer to small")
        if "parentName" in structt:
            # fill in the inherited data from the parent
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            s += self.genPackFields(parentStruct)
        #-- build the assignment of the data fields to the buffer
        s += self.genPackFields(structt)
        # if a funcion must be called before return 
        if localBuffAndUserFunct:
            s += "    return  "+callFuncName+"("+self.buffArrName
            s += ", "+self.buffPosName+");\n"
        else:
            s += "    return  "+self.buffPosName+";\n"
        s += "\n} // end\n"
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
        s += "    const "+self.intTypeName +" "+self.buffArrName+"Len = " + structLen
        s += ";\n"
        s += "          "+self.intTypeName +" "+self.buffPosName+"    = 0;\n"
        if localBuffAndUserFunct:
            s += "    "+self.bufTypeName+"  "+self.buffArrName+"["+self.buffArrName+"Len];\n"
        else:
            s += "    if ("+self.buffArrName+"Len > bufSize) return "+self.constErrBuffShort+";   "+self.makeLineComment("buffer to small")
        if "parentName" in structt:
            # fill in the inherited data from the parent
            prn           = structt["parentName"]
            parentStruct  = structDict[prn]
            #s += self.genPackFields(parentStruct)
            s += "    // call parent pack\n"
            s += "    "+self.buffPosName+" += "+prn+"::"+self.funcPackBaseName+"("
            s += self.makeCallFunArgList(parentStruct) 
            s += ");\n"
            s += "    // over write the values changed by this child\n"
        #-- build the assignment of the data fields to the buffer
        s += self.genPackFields(structt)
        # if a funcion must be called before return 
        if localBuffAndUserFunct:
            s += "    return  "+callFuncName+"("+self.buffArrName
            s += ", "+self.buffPosName+");\n"
        else:
            s += "    return  "+self.buffPosName+";\n"
        s += "\n} // end\n"
        return s

    def genPackMembersFunDecl(self,structt,namePrefix = ""):
        structnme     = structt["name"]
        fields        = structt["body"]
        parentArgs    = ""
        s  = "\n"
        # generate the comments
        s += self.codeCommentStart
        s += "This is a static function to pack data. "
        s += self.doxPre + "param buff[]"+self.doxPost+"    buffer into which data should be packed "
        s += self.doxPre + "param pos"+self.doxPost+"       start position in buffer "
        s += self.doxPre + "return if > 0"+self.doxPost+"   position in array of last extracted data"
        s += self.doxPre + "return if < 0"+self.doxPost+"   error in data stream "
        s += "\n" + self.codeCommentEnd +"\n"
        #-- build the argument list for the function
        args = "uint8_t  "+self.buffArrName+"[],"+self.intTypeName +" bufSize "
        #-- build the function call
        s += self.makeFuncDeclr(structt,self.intTypeName,namePrefix+self.funcPackBaseName,args)
        return s

        
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
        s1 = self.staticFunDecl + self.genCreateFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        s1 = self.staticFunDecl + self.genCreateFromBuffFunDecl(struct)
        s += "  "+addIndent(s1) + ";\n"
        # two version of static generated: a staic and non static
        s1 = self.genPackFunDecl(struct)
        if s1 != "":
            # change function to static
            pp = s1.find(self.funcPackBaseName)
            pp2 = s1.find(self.intTypeName,pp-15)
            s1  = s1[:pp2] + self.staticFunDecl +s1[pp2:]
            s += "  "+addIndent(s1) + ";\n"
        s1 = self.genPackMembersFunDecl(struct)
        if s1 != "":
            s += "  "+addIndent(s1) + ";\n"
        # generate unpack
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
            scc = self.simplifyAssignment(st,"12*MSG_ID+MLEN==2-$BUFF$[445+$$msg_id]-$destAddr")
            print (scc)
            llst = self.findParentFieldsUsingConsts(st)
            print(llst)
        return s,ss